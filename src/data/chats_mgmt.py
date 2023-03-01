from data import data
        


def is_new_chat(chat_id: int) -> bool:
    """
    Returns True if the chat is not in the bot's chats list.\n
    Otherwise, returns False.
    """
    for ent in data.DATA:
        if ent.get('chat_id') == chat_id:
            return False
    
    return True



def add_chat(chat_id: int) -> None:
    """
    Creates a chat entry in the bot's list.\n
    Carefully: a entry will be created, even if it is already in the bot's list.
    """
    users = []
    
    data.DATA.append({
        'chat_id': chat_id,
        'users': users
    })

    data.LOGGER.info(f"added new chat, chat_id={chat_id}")
    data.serialize()

