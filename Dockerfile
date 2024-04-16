FROM python:3.11-slim

WORKDIR /app

COPY --chown=user:user . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["python", "src/pdfchat/app.py"]
