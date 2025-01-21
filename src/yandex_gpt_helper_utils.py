import requests
from pathlib import Path
from os import getenv

FOLDER_ID = getenv("FOLDER_ID")
MOUNT_POINT = getenv("MOUNT_POINT")
BUCKET_OBJECT_KEY = getenv("BUCKET_OBJECT_KEY")

def get_answer(question, iam_token):
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {iam_token}"
    }
    data = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt",
        "messages": [
            {"role": "system", "text": _get_data_from_bucket()},
            {"role": "user", "text": question}
        ]
    }
    response = requests.post(url=url, headers=headers, json=data)

    if response.status_code != 200:
        return None

    alternatives = response.json()["result"]["alternatives"]
    final_alternatives = list(filter(
        lambda alternative: alternative["status"] == "ALTERNATIVE_STATUS_FINAL",
        alternatives
    ))

    return None if not final_alternatives else final_alternatives[0]["message"].get("text")

def recognize_text(base64_image, iam_token):
    url = "https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {iam_token}",
    }
    data = {
        "content": base64_image,
        "mimeType": "image/jpeg",
        "languageCodes": ["ru", "en"],
    }

    response = requests.post(url=url, headers=headers, json=data)
    if response.status_code != 200:
        return None

    text = response.json()["result"]["textAnnotation"]["fullText"].replace("-\n", "").replace("\n", " ")

    return None if not text else text

def _get_data_from_bucket():
    with open(Path("/function/storage", MOUNT_POINT, BUCKET_OBJECT_KEY), "r") as file:
        data = file.read()
    return data