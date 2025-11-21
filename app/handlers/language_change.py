from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from app.crud.users import CRUDUser
from app.db.base import AsyncSessionLocal
from config import settings
from app.services.ai_service import AIService

router = Router()

LANGUAGES = {
    "en": "English",
    "ru": "Русский",
    "uz": "O‘zbekcha"
}

def language_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    for code, name in LANGUAGES.items():
        buttons.append([InlineKeyboardButton(text=name, callback_data=f"set_lang:{code}")])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)  # обязательно передать пустой список
    return kb
@router.message(Command("lang"))
async def choose_language(message: Message):
    await message.answer("Выберите язык / Choose language / Tilni tanlang:", reply_markup=language_keyboard())

@router.callback_query(lambda c: c.data and c.data.startswith("set_lang:"))
async def set_language(cb: Message):
    lang_code = cb.data.split(":")[1]
    async with AsyncSessionLocal() as session:
        user = await CRUDUser.get_by_tg_id(session, cb.from_user.id)
        if not user:
            user = await CRUDUser.create(session, tg_id=cb.from_user.id, username=cb.from_user.username)
        meta = user.meta or {}
        meta["language"] = lang_code
        await CRUDUser.update(session, user, meta=meta)
    await cb.answer(f"Язык изменен на {LANGUAGES[lang_code]}", show_alert=True)
