from telegram import Update
from telegram.ext import ContextTypes

from datetime import datetime


from data.chats_mgmt import is_new_chat, add_chat
from data.users_mgmt import get_study_data, update_user_study_data, is_studies
from schedule.parser import get_schedule
from . import info
from service.logger import LOGGER
from service.settings import week_day_names
from phrases.phrases import START_MSG



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Updates the chat data and sends the starting information.
    """          
    if is_new_chat(update.effective_chat.id):
        add_chat(update.effective_chat.id)
        
    await update.effective_chat.send_message(START_MSG)



async def help(update: Update, context: ContextTypes.DEFAULT_TYPE, command_name: str = None) -> None:
    """
    Sends information about the use of the command if the command name is passed in the parameters.\n
    Otherwise, it will send information about the use of all commands.
    """
    msg = "Эта команда используется так:\n\n"
    instruction = ""

    if len(context.args) != 0:
        command_name = context.args[0]

    if not command_name:
        msg = "Вот, что я умею:\n\n"
        for command in info.COMMANDS.items():
            instruction += command[1].replace(' ~ ', '\n') + "\n\n"
    
    for command in info.COMMANDS.items():
        if command_name == command[0]:
            instruction = command[1].replace(' ~ ', '\n') + "\n\n"
            break

    if len(instruction) == 0:
        await update.effective_chat.send_message("Проверьте, правильно ли указано имя команды")
        LOGGER.info(f"HELP : could not find the command \"{command_name}\"")
        return
    
    await update.effective_chat.send_message(msg + instruction)
    


async def add_study_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user = update.effective_message.from_user

    args = context.args

    if len(args) == 0:
        await help(update, context, '/' + add_study_info.__name__)
        return
    
    update_user_study_data(chat_id, user, args)



async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args

    if len(args) == 0:
        await help(update, context, '/' + schedule.__name__)
        return
    

    week_num = datetime.today().isocalendar()[1]
    week = week_num % 2 # 0 = bottom, 1 = upper

    day_str = args[0]
    dt = datetime.now()
    today = dt.weekday()
    day_num = today

    if day_str not in week_day_names.keys():
        await update.message.reply_text("Не удалось определить день недели")
        return

    for day_name in week_day_names.keys():
        if day_str != day_name:
            continue

        if len(day_str) > 2:
            day_num += week_day_names.get(day_name) % 6
        else:
            day_num = week_day_names.get(day_name)

        break

    
    if day_num < today:
        week += 1 % 2
    
    user = update.effective_message.from_user
    chat_id = update.effective_message.chat_id  

    if is_studies(chat_id, user) == False:
        await update.effective_chat.send_message(
            "Сначала нужно указать данные о вас\nИспоьзуте комманду /add_study_info"
        )
        return

    study_data = get_study_data(chat_id, user)
    shedule_ = get_schedule(study_data, week, day_num)

    if shedule_ == None: 
        await update.message.reply_text("Не удалось получить расписание\nПроверьте ваши данные:\n\n" + str(study_data))
        await update.effective_chat.send_message("Если хотите обновить данные, используйте комманду /add_study_info")
        return




async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    
    if len(args) == 0:
        await help(update, context, '/' + remind.__name__)
        return
    
    await update.effective_chat.send_message("Эта команда находится в разработке")