import logging
from telegram import Update, Bot
from telegram.ext import ConversationHandler, filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler

import os
from supabase import create_client, Client

# url: str = os.environ.get("https://cwxkwruekonjpjqvpvyr.supabase.co")
# key: str = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3eGt3cnVla29uanBqcXZwdnlyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDM4NDMxODgsImV4cCI6MjAxOTQxOTE4OH0.fBWSlCajKKgQ3OrEr9M_hG_wFqzU6_Ajd7C_0NBrCG4")

url: str = "https://cwxkwruekonjpjqvpvyr.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3eGt3cnVla29uanBqcXZwdnlyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDM4NDMxODgsImV4cCI6MjAxOTQxOTE4OH0.fBWSlCajKKgQ3OrEr9M_hG_wFqzU6_Ajd7C_0NBrCG4"
supabase: Client = create_client(url, key)

bot = Bot(token="6932402333:AAHy4o5FG-tJoKDyfQvAJKWy23ThLowAlc4")


chat_list={}

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user = update.message.from_user.username
    data,count = supabase.table('chats').select('chat_id').eq('chat_id', chat_id).execute()
    
    if (data!=[]):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="user already exist!")
    else:
        supabase.table('chats').insert({"chat_id": chat_id,"userhandle":user}).execute()
        await context.bot.send_message(chat_id=update.effective_chat.id, text="created profile!")



async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Echo the user message."""
    chat_id = update.message.chat_id
    user = update.message.from_user
    print(chat_id,user.username)
    await update.message.reply_text(update.message.text)


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
            await bot.send_message(chat_id=chat_id, text="from @"+username+":\t"+update.message.text)

    
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
            await bot.send_message(chat_id=chat_id, text="@"+username+" left the chat")

    
    return ConversationHandler.END

if __name__ == '__main__':
    application = ApplicationBuilder().token('6932402333:AAHy4o5FG-tJoKDyfQvAJKWy23ThLowAlc4').build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    new_member_handler = CommandHandler('new', new_member)
    application.add_handler(new_member_handler)
    
    in_chat_handler = CommandHandler('in_chat', in_chat)
    application.add_handler(in_chat_handler)    
    
    chat_handler = ConversationHandler(
        entry_points=[CommandHandler('chat', chat)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, text)],
        },
        fallbacks=[CommandHandler("exit", exit)]
    )
    application.add_handler(chat_handler)
    
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling()