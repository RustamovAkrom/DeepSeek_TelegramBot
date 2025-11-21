from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from app.crud.users import CRUDUser
from app.db.base import AsyncSessionLocal

router = Router()

HELP_TEXT = {
    "en": "🤖 *Help*:\n/start - start bot\n/help - show this help\n/models - choose AI model\n/lang - change language",
    "ru": "🤖 *Помощь*:\n/start - начать бот\n/help - показать помощь\n/models - выбрать модель AI\n/lang - сменить язык",
    "uz": "🤖 *Yordam*:\n/start - botni boshlash\n/help - yordam ko‘rsatish\n/models - AI modelini tanlash\n/lang - tilni o‘zgartirish",
}

@router.message(Command("help"))
async def help_command(message: Message):
    async with AsyncSessionLocal() as session:
        user = await CRUDUser.get_by_tg_id(session, message.from_user.id)
        lang = "en"
        if user and user.meta:
            lang = user.meta.get("language", "en")
        await message.answer(HELP_TEXT.get(lang, HELP_TEXT["en"]))
