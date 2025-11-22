from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.crud.users import CRUDUser
from app.db.base import get_session
from app.locales.translator import i18n

router = Router()


@router.message(Command("help"))
async def help_cmd(message: Message):
    async with get_session() as session:
        user = await CRUDUser.get_by_tg_id(session, message.from_user.id)

        lang = user.get_language()
        print(lang)

        await message.answer(i18n.t(lang, "help"))
