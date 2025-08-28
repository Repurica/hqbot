import os
import json
import requests
from dotenv import load_dotenv
import functions.command as command
import functions.chat as chat
# Only load .env in local development
if os.environ.get('AWS_LAMBDA_FUNCTION_NAME') is None:
    load_dotenv()

bot_token = os.environ.get("BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{bot_token}"

def send_message(chat_id, text, parse_mode=None):
    url = f"{TELEGRAM_API_URL}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    if parse_mode:
        payload["parse_mode"] = parse_mode
    requests.post(url, json=payload)



virtual_chat = chat.Chat(TELEGRAM_API_URL)



def lambda_handler(event, context):
    body = event.get("body")
    if body is None:
        return {"statusCode": 400, "body": "No body found"}

    update = json.loads(body)
    message = update.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")

    if not chat_id:
        return {"statusCode": 200, "body": "No chat_id"}

    if text.startswith("/start"):
        send_message(
            chat_id,
            "Welcome to smuhq bot! This bot is designed to better facilitate HQ!\n\n"
            "Available Commands:\n\n"
            "<strong>chat</strong>\n"
            "/chat - join a virtual chat group\n"
            "any message - broadcast message to those who are in chat\n"
            "/in_chat - list all users in chat\n"
            "/exit - exit chat group",
            parse_mode="HTML"
        )
    else:
        virtual_chat.add_message(message, text)
        virtual_chat.send_message(chat_id)
        # send_message(chat_id, {text})
        

    return {"statusCode": 200, "body": "ok"}
