from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from random import choice

from data.users_mgmt import extract_status_change, add_user, delete_user

from phrases.phrases import *




async def greet_chat_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    result = extract_status_change(update.chat_member)
    if result is None:
        return

    was_member, is_member = result

    cause_mention = update.chat_member.from_user.mention_html()
    member = update.chat_member.new_chat_member.user
    member_mention = member.mention_html()


    if not was_member and is_member:
        response = choice(GREETINGS).format(member_mention, cause_mention)
        add_user(update.effective_chat.id, member)

    elif was_member and not is_member:
        response = choice(GOODBYES).format(cause_mention, member_mention)
        delete_user(update.effective_chat.id, member)


    await update.effective_chat.send_message(
        response,
        parse_mode=ParseMode.HTML,
    )