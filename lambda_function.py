import os
import json
import requests
from dotenv import load_dotenv
import functions.chat as chat
# Only load .env in local development
if os.environ.get('AWS_LAMBDA_FUNCTION_NAME') is None:
    load_dotenv()

bot_token = os.environ.get("BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{bot_token}"





virtual_chat = chat.Chat(TELEGRAM_API_URL)



def lambda_handler(event, context):
    body = event.get("body")
    if body is None:
        return {"statusCode": 400, "body": "No body found"}


    # message = {'message_id': 1706, 'from': {'id': 1272231156, 'is_bot': False, 'first_name': 'Jinming', 'last_name': 'Cao', 'username': 'repurika', 'language_code': 'zh-hans'}, 'chat': {'id': 1272231156, 'first_name': 'Jinming', 'last_name': 'Cao', 'username': 'repurika', 'type': 'private'}, 'date': 1756377079, 'text': '123'}

    update = json.loads(body)
    message = update.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    username = message.get("from", {}).get("username")
    text = message.get("text", "")

    if not chat_id:
        return {"statusCode": 200, "body": "No chat_id"}

    if text.startswith("/start"):
        virtual_chat.start(chat_id)
    elif text.startswith("/chat"):
        virtual_chat.chat(chat_id, username, text)
    elif text.startswith("/in_chat"):
        virtual_chat.in_chat(chat_id, text)
    elif text.startswith("/exit"):
        virtual_chat.exit(chat_id, text)
    
    else:
        virtual_chat.normal_message(chat_id, username, text)

    return {"statusCode": 200, "body": "ok"}
