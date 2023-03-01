from telegram import Update
from telegram.ext import ContextTypes

from data.users_mgmt import add_user



async def add_new_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    A wrapper for add_user with effective chat id
    """
    if add_user(update.effective_chat.id, update.message.from_user) == False:
        await update.effective_chat.send_message("Пожалуйста, напишите команду /start, чтобы я мог нормально работать")