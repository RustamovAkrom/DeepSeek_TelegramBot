from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

from app.crud.users import CRUDUser
from app.db.base import get_session

router = Router()

HELP_TEXT = """
Hello! I'm your AI assistant 🤖

Here are the commands you can use:
/start — start interacting with the bot
/help — show this help message
/history — view your AI query history
/clear_history — clear your entire history
/set_language — choose your language
/set_model — choose AI model

Just send a message and I'll generate a response for you!
"""


@router.message(Command("help"))
async def help_cmd(message: Message):
    async with get_session() as session:
        user = await CRUDUser.get_by_tg_id(session, message.from_user.id)
        if user:
            text = f"Hello, {user.first_name}!\n" + HELP_TEXT
        else:
            text = HELP_TEXT

        await message.answer(text)
