import logging
from telegram import Update, Bot
from telegram.ext import ConversationHandler, filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
from dotenv import load_dotenv
import os
# below import from your .py file, must import as functions
from functions.chat import chat, in_chat, exit, text
# above import from your .py file, must import as functions


# from supabase import create_client, Client


load_dotenv()
# url: str = os.getenv("SUPABASE_URL")
# key: str = os.getenv("SUPABASE_KEY")
# supabase: Client = create_client(url, key)

bot = Bot(token=os.getenv("BOT_TOKEN"))


# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, parse_mode='HTML', 
                                   text=
"Welcome to smuhq bot! This bot is designed to better facilitate HQ!" 
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




if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    print("HQ BOT RUNNING!")
    
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
    print("HQ BOT RUNNING!")
    
