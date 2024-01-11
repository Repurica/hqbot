# below are compulsory imports
import os
from telegram import Update,Bot
from telegram.ext import ConversationHandler, ContextTypes
from dotenv import load_dotenv
load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
# above are compulsory imports


chat_list={}


async def in_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global chat_list
    text="Currently in chat:\n\n"
    
    for username, chat_id in chat_list.items():
            text+="@"+username+"\n"
    
    await update.message.reply_text(text[:-1])


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global chat_list
    chat_list[update.message.from_user.username]=update.message.chat_id
    text="You are in chat now! Currently in chat:\n\n"
    
    for username, chat_id in chat_list.items():
            text+="@"+username+"\n"
            if chat_id != update.message.chat_id:
                await bot.send_message(chat_id=chat_id, text="@"+update.message.from_user.username+" joined the chat")
    
    await update.message.reply_text(text[:-1])

    return 0

async def text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global chat_list
    global bot
    
    for username, chat_id in chat_list.items():
        if chat_id != update.message.chat_id:
            await bot.send_message(chat_id=chat_id, text="from @"+update.message.from_user.username+":\t"+update.message.text)

    
    return 0

async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    """Exits and ends the conversation."""

    global bot
    global chat_list

    await update.message.reply_text(
        "End chat"
    )
    
    del chat_list[update.message.from_user.username]
    
        
    for username, chat_id in chat_list.items():
        if chat_id != update.message.chat_id:
            await bot.send_message(chat_id=chat_id, text="@"+update.message.from_user.username+" left the chat")

    
    return ConversationHandler.END