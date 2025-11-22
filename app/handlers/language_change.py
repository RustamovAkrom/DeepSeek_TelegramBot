from aiogram import Router, F
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    Message,
)
from aiogram.filters import Command

from app.crud.users import CRUDUser
from app.services.user_service import ensure_user
from app.db.base import get_session
from app.locales.translator import i18n

router = Router()


def lang_keyboard(lang: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=i18n.t(lang, "btn_en"), callback_data="lang:en"
                )
            ],
            [
                InlineKeyboardButton(
                    text=i18n.t(lang, "btn_ru"), callback_data="lang:ru"
                )
            ],
            [
                InlineKeyboardButton(
                    text=i18n.t(lang, "btn_uz"), callback_data="lang:uz"
                )
            ],
        ]
    )


@router.message(Command("language"))
async def choose_language(message: Message):
    async with get_session() as session:
        user = await ensure_user(session, message.from_user)

        lang = user.get_language()

        await message.answer(
            i18n.t(lang, "language_choose"), reply_markup=lang_keyboard(lang)
        )


@router.callback_query(F.data.startswith("lang"))
async def set_language(call: CallbackQuery):
    lang_code = call.data.split(":")[1]

    async with get_session() as session:
        user = await ensure_user(session, call.from_user)
        await CRUDUser.update_meta(session, user, {"language": lang_code})

        await call.answer(i18n.t(lang_code, "language_updated"))
        await call.message.edit_text(i18n.t(lang_code, "help"))
