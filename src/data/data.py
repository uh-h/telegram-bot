import sys
import json
from json import JSONDecodeError
from typing import Tuple

from service.logger import LOGGER


sys.path.append("..")
DATA_PATH = r'src/data/data.json'
ENCODING = 'utf8'
DATA = []



def serialize(path: str = DATA_PATH, encd: str = ENCODING) -> None:
    """
    Serializes data about the chats in which the bot consists.
    """
    try:
        file = open(path, "w", encoding=encd)
        json.dump(DATA, file, indent=4, ensure_ascii=False)
        file.close()
    except:
        LOGGER.exception("failsed to serialize data")




def deserialize(path: str = DATA_PATH, encd: str = ENCODING) -> None:
    """
    Deserializes data about the chats in which the bot consists.
    """
    global DATA
    try:
        file = open(path, 'r+', encoding=encd)
        DATA = json.load(file)
        file.close()
    except JSONDecodeError:
        LOGGER.exception("unable to access the data")
        return




def get_chats() -> list:
    """
    Returns a list of chat's ids in which there is the bot.
    """
    chats = []
    chats.append(chat.get('chat_id') for chat in DATA)

    if chats:
        return chats
    else:
        return []



def get_users(chat_id: int) -> Tuple[int, list]:
    """
    Returns list of users in the chat's id is specified.\n
    Otherwise, return list of all users in all chats in witch there is the bot.\n
    If the chat is not found, returns empty list.
    """

    for chat_pos, chat in enumerate(DATA):
        if chat.get('chat_id') == chat_id:
            return chat_pos, chat.get('users')
        
    LOGGER.critical(f"could not found the chat whit id={chat_id}")
    return None, None



def get_user(chat_id: int, user_id: int) -> dict:
    chat_pos, users = get_users(chat_id)
    
    for user in users:
        if user.get('id') == user_id:
            return user
    
    LOGGER.critical(f"could not found the user in chat, chat_id='{chat_id}', user_id={user_id}")
    return None



def update_user_data(chat_id: int, user_id: int, key, value) -> None:
    chat_pos, users = get_users(chat_id)

    for user in users:
        if user.get('id') == user_id:
            user.update({key: value})
