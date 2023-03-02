from telegram import User, ChatMember, ChatMemberUpdated

from typing import Optional, Tuple

from data import data
from service.logger import LOGGER
from service.settings import user_study_data_template



def add_user(chat_id: int, user: User) -> bool:
    """
    Adds information about the user in the chat with the corresponding id in bot's data list.
    """
    chat_pos, users = data.get_users(chat_id)

    if users == None:
        return False

    for user_ in users:
        if user.id == user_.get('id'):
            return True

    
    user_dict = user.to_dict()
    user_dict.update(user_study_data_template)
    users.append(user_dict)

    data.DATA[chat_pos].update({'users': users})
    data.serialize()
    LOGGER.info(f"added new user, chat_id='{chat_id}', user_id='{user.id}'")

    return True
 



def delete_user(chat_id: int, user: User) -> None:
    users = data.get_users(chat_id)

    for user_ in users:
        if user_.get('id') == user.id:
            users.remove(user_)
            return

    LOGGER.info(f"could not find user, chat_id={chat_id}, user_id={user.id}")



def get_study_data(chat_id: int, user: User) -> dict:
    user_ = data.get_user(chat_id, user.id)
    study_data = {}

    for key in user_study_data_template.keys():
        study_data.update({key: user_.get(key)})

    return study_data


    
def update_user_study_data(chat_id: int, user: User, study_data: list) -> None:
    keys = list(user_study_data_template.keys())

    for i in range(len(study_data)):
        data.update_user_data(chat_id, user.id, keys[i], study_data[i])

    data.serialize()
    LOGGER.info(f"Added information about studying, chat_id='{chat_id}', user_id='{user.id}', data='{study_data}'")
        




def is_studies(chat_id: int, user: User) -> bool:
    user_ = data.get_user(chat_id, user.id)

    if user_ == None:
        return False
    
    for key in user_study_data_template.keys():
        if user_.get(key) == None:
            return False
    
    return True



# нужно переписать менеджемент. Подумать над тем, чтобы пробегать дату через enumerate и возвращать индекс. Получать доступ к дате через этот индекс.
def change_state(chat_id: str, user: User) -> None:
    for chat in data.DATA:
        if chat.get('chat_id') == chat_id:
            chat.get()
        



def extract_status_change(chat_member_update: ChatMemberUpdated) -> Optional[Tuple[bool, bool]]:
    status_change = chat_member_update.difference().get("status")
    old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))

    if status_change is None:
        return None

    old_status, new_status = status_change
    was_member = old_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (old_status == ChatMember.RESTRICTED and old_is_member is True)

    is_member = new_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (new_status == ChatMember.RESTRICTED and new_is_member is True)

    return was_member, is_member