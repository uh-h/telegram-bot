from telegram.ext import CommandHandler, MessageHandler, ChatMemberHandler, Application, filters

from service.bot_info import TOKEN
from handlers.commands import private, public
from handlers import messages as msg_handler
from data import data



def main():
    app = Application.builder().token(TOKEN).build()

    handlers = [
        ChatMemberHandler(private.greet_chat_members, ChatMemberHandler.CHAT_MEMBER),

        CommandHandler("start", public.start),
        CommandHandler("help", public.help),
        CommandHandler("add_study_info", public.add_study_info),
        CommandHandler("schedule", public.schedule),
        CommandHandler("remind", public.remind),
        
        MessageHandler(filters.ALL, msg_handler.add_new_user),
    ]

    app.add_handlers(handlers)
    data.deserialize()
    app.run_polling()




if __name__=='__main__':
    main()
