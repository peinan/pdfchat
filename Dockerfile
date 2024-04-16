FROM python:3.11-slim

RUN useradd -m -u 1000 user
USER user

ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=user . $HOME/app

EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["python", "src/pdfchat/app.py"]
