import logging
from telegram import Update, Bot
from telegram.ext import ConversationHandler, filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler

import os
# from supabase import create_client, Client


# url: str = os.getenv("SUPABASE_URL")
# key: str = os.getenv("SUPABASE_KEY")
# supabase: Client = create_client(url, key)

bot = Bot(token=os.getenv("BOT_TOKEN"))

chat_list={}

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, parse_mode='HTML', 
                                   text=
"Welcome to smuhq bot! This bot is designed to better facilit HQ!" 
"\n\nAvailable Commands:\n\n"  
"<strong>chat</strong>\n" 
"/chat - join a virtual chat group\n"
"any message - broadcast message to those who are in chat\n"
"/in_chat - list all users in chat\n"
"/exit - exit chat group" )

# async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # chat_id = update.message.chat_id
    # user = update.message.from_user.username
    # data,count = supabase.table('chats').select('chat_id').eq('chat_id', chat_id).execute()
    
    # if (data!=[]):
    #     await context.bot.send_message(chat_id=update.effective_chat.id, text="user already exist!")
    # else:
    #     supabase.table('chats').insert({"chat_id": chat_id,"userhandle":user}).execute()
    #     await context.bot.send_message(chat_id=update.effective_chat.id, text="created profile!")



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

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    # new_member_handler = CommandHandler('new', new_member)
    # application.add_handler(new_member_handler)
    
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