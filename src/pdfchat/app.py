import time
from dataclasses import dataclass
from pathlib import Path

import gradio as gr
from gradio_pdf import PDF
from loguru import logger

MODEL_CALM2 = "cyberagent/calm2"


@dataclass
class Chat:
    query: str
    response: str | None

    def to_list(self) -> list[str, str]:
        return [self.query, self.response]


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


def open_file(file_path: str) -> str:
    file_path = Path(file_path)
    if file_path.suffix == ".txt":
        text = file_path.read_text()
    elif file_path.suffix == ".pdf":
        text = "WARNING: PDF file is not supported yet."
    else:
        text = "WARNING: Unsupported file format."

    return text


def get_response(query: str, document: str | None) -> str:
    response = ""
    if not document:
        response = "No document is uploaded. Please upload a document."
    else:
        response = f"Your document: {document}"

    return response


def bot(history: ChatHistory, query: str, file_path: str) -> ChatHistory:
    history = ChatHistory(history)
    document = open_file(file_path) if file_path else None
    response = get_response(query, document)
    history.add_chat(Chat(query=query, response=response))
    logger.info(history)

    history.clear_last_response()
    for char in response:
        history[-1].response += char
        time.sleep(0.02)
        yield history


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
                temperature_slider = gr.Slider(
                    minimum=0.1, maximum=1.0, value=0.5, label="Temperature"
                )
                temperature_slider.change(lambda x: x, [temperature_slider])
                top_p_slider = gr.Slider(
                    minimum=0.1, maximum=1.0, value=0.5, label="Top P"
                )
                top_p_slider.change(lambda x: x, [top_p_slider])
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
                    fn=bot,
                    inputs=[chatbot, text_box, file_box],
                    outputs=chatbot,
                )
    examples = gr.Examples(
        examples=[
            [
                "data/sample.pdf",
                "胃がん手術の説明書の要点を箇条書きで要約してください",
            ]
        ],
        inputs=[file_box, text_box],
        outputs=[],
        fn=lambda model_name, document: None,
    )

app.queue().launch()
