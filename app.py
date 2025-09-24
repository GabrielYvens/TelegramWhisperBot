from flask import Flask, request, jsonify
import requests
import whisper
import os

app = Flask(__name__)

# Carregar modelo Whisper
model = whisper.load_model("small")  # ou "medium" para mais precisão

# Token do Telegram (use variável de ambiente)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

@app.route("/", methods=["POST"])
def receber_audio():
    data = request.json
    file_id = data.get("file_id")
    chat_id = data.get("chat_id")

    if not file_id or not chat_id:
        return jsonify({"error": "Dados incompletos"}), 400

    # Baixar arquivo do Telegram
    file_info = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getFile?file_id={file_id}").json()
    file_path = file_info['result']['file_path']
    audio_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"
    r = requests.get(audio_url)
    with open("temp.ogg", "wb") as f:
        f.write(r.content)

    # Transcrever áudio
    result = model.transcribe("temp.ogg")
    texto = result["text"]

    return jsonify({"texto": texto, "chat_id": chat_id})
