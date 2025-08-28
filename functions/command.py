# below are compulsory imports
import os
from telegram import Update, Bot
from telegram.ext import ConversationHandler, ContextTypes
from dotenv import load_dotenv
import random
load_dotenv()
bot_token = os.environ.get("BOT_TOKEN")
# above are compulsory imports

chat_list = {}

async def command_handler(chat_id,text):
    if text=='/in_chat':
        await in_chat(chat_id)
    elif text=='/chat':
        await chat(chat_id)
    elif text=='/exit':
        await exit(chat_id)
    else:
        await bot.send_message(chat_id=chat_id, text="Unknown command")


async def in_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global chat_list
    text = "Currently in chat:\n\n"

    for username, (chat_id, icon) in chat_list.items():
        text += f"@{username} {icon}\n"

    await update.message.reply_text(text[:-1])


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global chat_list
    current_icon=get_user_icon(update.message.from_user.username)
    chat_list[update.message.from_user.username] = (update.message.chat_id, current_icon)
    text = "You are in chat now! Currently in chat:\n\n"

    for username, (chat_id, icon) in chat_list.items():
        text += f"@{username} {icon}\n"
        if chat_id != update.message.chat_id:
            await bot.send_message(chat_id=chat_id, text=f"@{update.message.from_user.username} {current_icon} joined the chat")

    await update.message.reply_text(text[:-1])

    return 0


async def text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global chat_list
    global bot

    for username, (chat_id, icon) in chat_list.items():
        if chat_id != update.message.chat_id:
            await bot.send_message(chat_id=chat_id,
                                   text=f"from @{update.message.from_user.username} {icon}: {update.message.text}")

    return 0


async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Exits and ends the conversation."""
    global bot
    global chat_list

    await update.message.reply_text("End chat")

    del chat_list[update.message.from_user.username]

    for username, (chat_id, icon) in chat_list.items():
        if chat_id != update.message.chat_id:
            await bot.send_message(chat_id=chat_id, text=f"@{update.message.from_user.username} left the chat")

    return ConversationHandler.END


def get_user_icon(username: str) -> str:
    """Assigns a unique animal icon for each user."""
    icons = [
        "🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐮", "🐷", "🐸", "🐵", "🐔", "🐧", "🐦", "🐤", "🦆",
        "🦅", "🦉", "🦇", "🐺", "🐗", "🐴", "🦄", "🐝", "🐛", "🦋", "🐌", "🐞", "🐜", "🦟", "🦗", "🕷️", "🦂", "🐢", "🐍", "🦎",
        "🦖", "🦕", "🐙", "🦑", "🦐", "🦞", "🦀", "🐡", "🐠", "🐟", "🐬", "🐳", "🐋", "🦈", "🐊", "🐅", "🐆", "🦓", "🦍", "🦧",
        "🐘", "🦛", "🦏", "🐪", "🐫", "🦒", "🦘", "🐃", "🐂", "🐄", "🐎", "🐖", "🐏", "🐑", "🦙", "🐐", "🦌", "🐕", "🐩", "🦮",
        "🐕‍🦺", "🐈", "🐈‍⬛", "🐓", "🦃", "🦚", "🦜", "🦢", "🦩", "🕊️", "🐇", "🦝", "🦨", "🦡", "🦦", "🦥", "🐁", "🐀", "🐿️",
        "🦔", "🐾"
    ]
    icon = random.choice(icons)
    icons.remove(icon)
    return icon
