import json
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path

import gradio as gr
import requests
from gradio_pdf import PDF
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.qdrant import Qdrant
from loguru import logger
from pypdf import PdfReader

MODEL_CALM2 = "cyberagent/calm2-7b-chat"
text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1000,
    chunk_overlap=0,
)
QDRANT_MODE = "local"
if QDRANT_MODE == "local":
    QDRANT_CLIENT_CONFIG = {
        "path": "./local_qdrant",
    }
elif QDRANT_MODE == "cloud":
    QDRANT_CLIENT_CONFIG = {
        "url": os.environ.get("QDRANT_URL"),
        "api_key": os.environ.get("QDRANT_API_KEY"),
    }
    if not QDRANT_CLIENT_CONFIG["url"] or not QDRANT_CLIENT_CONFIG["api_key"]:
        raise ValueError(
            "Please set the QDRANT_URL and QDRANT_API_KEY environment variables."
        )
COLLECTION_NAME = "pdfchat"
PROMPT_TEMPLATE = """以下の文脈を利用して、最後の質問に答えなさい。
答えがわからない場合は、わからないと答えてください。

【文脈】
{context}

【質問】
{question}

【答え】
"""
LLM_URL = os.environ.get("PDFCHAT_LLM_URL")


@dataclass
class Chat:
    query: str
    response: str | None

    def to_list(self) -> list[str, str]:
        return [self.query, self.response]

    def to_dict(self) -> dict[str, str]:
        return {"query": self.query, "response": self.response}


@dataclass
class ChatHistory:
    history: list[Chat]

    def __init__(self, history: list[tuple[str, str] | list[str, str]] | None = None):
        if history is None:
            self.history = []
        else:
            self.history = [Chat(*chat) for chat in history]

    def __iter__(self):
        return iter([chat.to_list() for chat in self.history])

    def __getitem__(self, index: int) -> Chat:
        return self.history[index]

    def add_chat(self, chat: Chat):
        self.history.append(chat)

    def clear_last_response(self):
        self.history[-1].response = ""

    def to_json(self) -> str:
        return json.dumps(
            [chat.to_dict() for chat in self.history], ensure_ascii=False, indent=4
        )


def open_file(file_path: str) -> str:
    file_path = Path(file_path)
    if file_path.suffix == ".txt":
        text = file_path.read_text()
    elif file_path.suffix == ".pdf":
        text = parse_pdf(file_path)
    else:
        text = "WARNING: Unsupported file format."

    return text


def parse_pdf(file_path: Path, backend="pypdf") -> str:
    reader = PdfReader(file_path)
    contents = "".join([page.extract_text() for page in reader.pages])

    contents = re.sub(r"[ 　]+\n[ 　]+", "\n", contents)
    contents = re.sub(r"[ 　]+\n", "\n", contents)
    contents = re.sub(r"\n[ 　]+", "\n", contents)
    contents = re.sub(r"[^。\n]\n", "", contents)
    contents = re.sub(r"[\w、（）]\n[\w、（）]", "", contents)
    contents = re.sub(r"\n{3,}", "\n\n", contents)

    return contents


def get_response(prompt: str) -> str:
    response = requests.post(
        LLM_URL,
        json={
            "prompt": prompt,
            "max_new_tokens": 3072,
        },
    ).json()

    return response


def retrieve_relevant_documents(query: str, document: str | None) -> list[str]:
    if not document:
        return "No document is uploaded. Please upload a document."

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("Please set the OPENAI_API_KEY environment variable.")

    documents = text_splitter.split_text(document)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    db = Qdrant.from_texts(
        texts=documents,
        embedding=embeddings,
        **QDRANT_CLIENT_CONFIG,
    )
    retriever = db.as_retriever()
    relevant_documents = [
        doc.page_content for doc in retriever.get_relevant_documents(query)
    ]

    return relevant_documents


def build_prompt(query: str, context: str) -> str:
    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"],
    ).format(context=context, question=query)

    return prompt


def main(history: ChatHistory, query: str, file_path: str | None) -> ChatHistory:
    history = ChatHistory(history)
    document = open_file(file_path) if file_path else None
    relevant_documents = retrieve_relevant_documents(query=query, document=document)
    prompt = build_prompt(query=query, context="\n\n".join(relevant_documents))
    response_message = get_response(prompt)["message"]
    history.add_chat(Chat(query=query, response=response_message))
    logger.info(history)

    history.clear_last_response()
    for char in response_message:
        history[-1].response += char
        time.sleep(0.01)
        yield history


def save_chat_history(history: ChatHistory = []) -> str:
    history = ChatHistory(history)
    file_path = Path("history.json")
    with open(file_path, "w") as f:
        f.write(history.to_json())

    return str(file_path)


with gr.Blocks() as app:
    gr.Markdown("# Chat with PDF")
    with gr.Row():
        with gr.Column(scale=35):
            model_name = gr.Dropdown(
                choices=[MODEL_CALM2],
                value=MODEL_CALM2,
                label="Model",
            )
            file_box = PDF(
                label="Document",
            )
            with gr.Accordion("Parameters", open=False):
                gr.Markdown("⚠️Warning⚠️ Not implemented yet")
                temperature_slider = gr.Slider(
                    minimum=0.1, maximum=1.0, value=0.5, label="Temperature"
                )
                temperature_slider.change(lambda x: x, [temperature_slider])
                top_p_slider = gr.Slider(
                    minimum=0.1, maximum=1.0, value=0.5, label="Top P"
                )
                top_p_slider.change(lambda x: x, [top_p_slider])
            with gr.Accordion("Save Chat History", open=False):
                history_file = gr.File()
        with gr.Column(scale=65):
            chatbot = gr.Chatbot(
                bubble_full_width=False,
                height=650,
                show_copy_button=True,
                avatar_images=(
                    Path("data/avatar-user.png"),
                    Path("data/avatar-bot.png"),
                ),
            )
            text_box = gr.Textbox(
                lines=2,
                label="Chat message",
                show_label=False,
                placeholder="Type your message here",
                container=False,
            )
            with gr.Row():
                clear_button = gr.ClearButton(
                    [text_box, chatbot, file_box], variant="secondary", size="sm"
                )
                submit_button = gr.Button("Submit", variant="primary", size="sm")
                submit = submit_button.click(
                    fn=main,
                    inputs=[chatbot, text_box, file_box],
                    outputs=chatbot,
                ).then(
                    lambda history: save_chat_history(history),
                    inputs=[chatbot],
                    outputs=history_file,
                )
    examples = gr.Examples(
        examples=[
            [
                "data/sample.pdf",
                "胃がん手術の説明書の要点を箇条書きで要約してください",
            ],
            [
                "data/sample2.pdf",
                "面会時間について教えてください",
            ],
        ],
        inputs=[file_box, text_box],
        outputs=[],
        fn=lambda model_name, document: None,
    )

app.queue().launch()
