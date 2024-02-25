import time
from dataclasses import dataclass
from pathlib import Path

import gradio as gr
from icecream import ic

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


def open_file(file_path: str) -> str:
    file_path = Path(file_path)
    if file_path.suffix == ".txt":
        text = file_path.read_text()
    elif file_path.suffix == ".pdf":
        text = "WARNING: PDF file is not supported yet."
    else:
        gr.exit("Unsupported file type.")

    return text


def bot(history: ChatHistory, query: str, file_path: str) -> ChatHistory:
    history = ChatHistory(history)
    if not file_path:
        history.add_chat(Chat(query=query, response=None))
        return history
    document = open_file(file_path)
    history.add_chat(Chat(query=query, response=document))
    ic(history)

    # TODO: use streaming inference
    return history


with gr.Blocks() as app:
    with gr.Row():
        with gr.Column(scale=0.4):
            model_name = gr.Dropdown(
                choices=[MODEL_CALM2],
                value=MODEL_CALM2,
                label="Model",
            )
            file_box = gr.File(
                label="Document",
                file_types=[".pdf", ".txt"],
                file_count="single",
                container=False,
            )
            gr.Examples(
                examples=[["data/sample.txt"], ["data/sample.pdf"]],
                inputs=[file_box],
                outputs=[],
                fn=lambda model_name, document: None,
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
        with gr.Column(scale=0.6):
            chatbot = gr.Chatbot(
                bubble_full_width=False,
                height=650,
            )
            ic(chatbot)
            with gr.Row():
                text_box = gr.Textbox(
                    scale=0.9,
                    show_label=False,
                    placeholder="Type your message here",
                    container=False,
                )
                submit_button = gr.Button("Submit", scale=0.1, variant="primary")
                submit = submit_button.click(
                    fn=bot,
                    inputs=[chatbot, text_box, file_box],
                    outputs=chatbot,
                )

app.queue().launch(debug=True)
