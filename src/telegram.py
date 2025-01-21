import requests
from os import getenv

TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
TELEGRAM_FILE_URL = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}"

def send_message(reply_text, input_message):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    data = {
        "chat_id": input_message["chat"]["id"],
        "text": reply_text,
        "reply_parameters": {
            "message_id": input_message["message_id"]
        }
    }

    requests.post(url=url, json=data)

def get_file_path(file_id):
    url = f"{TELEGRAM_API_URL}/getFile"
    data = { "file_id": file_id }
    response = requests.get(url=url, params=data)

    return None if response.status_code != 200 else response.json()["result"].get("file_path")

def get_image(file_path):
    url = f"{TELEGRAM_FILE_URL}/{file_path}"
    response = requests.get(url=url)

    return None if response.status_code != 200 else response.content
