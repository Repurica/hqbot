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



    update = json.loads(body)
    message = update.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    username = message.get("from", {}).get("username")
    
    # virtual_chat.send_message(chat_id, message)

    if not chat_id:
        return {"statusCode": 200, "body": "No chat_id"}

    if 'text' in message:

        text = message.get("text", "")

        if text.startswith("/start"):
            virtual_chat.start(chat_id)
        elif text.startswith("/chat"):
            virtual_chat.chat(chat_id, username)
        elif text.startswith("/in_chat"):
            virtual_chat.in_chat(chat_id)
        elif text.startswith("/exit"):
            virtual_chat.exit(chat_id, username)
    
        else:
            virtual_chat.normal_message(chat_id, username, text)
    elif 'photo' in message:
        file_id = message['photo'][-1]['file_id']
        caption = message.get('caption', '')
        virtual_chat.forward_photo(chat_id, username, file_id, caption)
    elif 'sticker' in message:
        file_id = message['sticker']['file_id']
        caption = message.get('caption', '')
        virtual_chat.forward_sticker(chat_id, username, file_id, caption)
    elif 'video_note' in message:
        file_id = message['video_note']['file_id']
        caption = message.get('caption', '')
        virtual_chat.forward_tele_bubble(chat_id, username, file_id, caption)
    return {"statusCode": 200, "body": "ok"}
