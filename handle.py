import json
from base64 import b64encode
from telegram import send_message, get_file_path, get_image
from  yandex_gpt_helper_utils import get_answer, recognize_text

CANT_ANSWER = "Я не смог подготовить ответ на экзаменационный вопрос."
CAN_HANDLE_ONLY_TEXT_OR_PHOTO = "Я могу обработать только текстовое сообщение или фотографию."
HANDLE_GLOBAL_COMMAND = "Я помогу подготовить ответ на экзаменационный вопрос по дисциплине 'Операционные системы'. Пришлите мне фотографию с вопросом или наберите его текстом."

def handler(event, context):
    update = json.loads(event["body"])
    message = update.get("message")

    if message:
        _message(message, context.token["access_token"])

    return { "statusCode": 200 }

def _message(message, iam_token):
    if (text := message.get("text")) and text in {"/start", "/help"}:
        send_message(HANDLE_GLOBAL_COMMAND, message)
    elif text := message.get("text"):
        _text_message(text, message, iam_token)
    elif image := message.get("photo"):
        _photo_message(image, message, iam_token)
    else:
        send_message(CAN_HANDLE_ONLY_TEXT_OR_PHOTO, message)

def _photo_message(tg_photo, message, iam_token):
    image_path = get_file_path(tg_photo[-1]["file_id"])
    image = get_image(image_path)
    text = recognize_text(b64encode(image).decode("utf-8"), iam_token)

    send_message(CANT_ANSWER, message) if not text else _text_message(text, message, iam_token)


def _text_message(text, message, iam_token):
    answer = get_answer(text, iam_token)
    send_message(CANT_ANSWER if not answer else answer, message)
