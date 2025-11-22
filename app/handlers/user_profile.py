from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_session
from app.services.user_service import ensure_user
from app.utils.base import send_long
from app.crud.history import CRUDHistory

router = Router()


# User Profile
@router.message(Command("profile"))
async def show_profile(message: Message, state: FSMContext):
    async with get_session() as session:
        user = await ensure_user(session, message.from_user)
        user_profile = user

        # For Markdown V2
        username_md = user_profile.username or "No username"
        first_name_md = user_profile.first_name or "No first name"
        last_name_md = user_profile.last_name or "No last name"
        language_md = user_profile.language_code or "Unknown"
        tg_id = user_profile.tg_id

        profile_text = (
            f"<b>Profile</b>\n"
            f"<b>ID:</b> <code>{tg_id}</code>\n"
            f"<b>First name:</b> <code>{first_name_md}</code>\n"
            f"<b>Last name:</b> <code>{last_name_md}</code>\n"
            f"<b>Username:</b> @{username_md}\n"
            f"<b>Language:</b> <code>{language_md}</code>"
        )

        buttons = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="History", callback_data="history")]
            ]
        )

        await message.answer(
            text=profile_text, reply_markup=buttons, parse_mode=ParseMode.HTML
        )


# User History
@router.callback_query(F.data == "history")
async def show_history(message: Message, state: FSMContext):
    async with get_session() as session:
        user = await ensure_user(session, message.from_user)
        history = await CRUDHistory.list_user_history(session, user.id)
        text = "🧾 Your History:\n\n" + "\n".join(
            [f"{i+1}. {h.role}: {h.content}" for i, h in enumerate(history)]
        )

        buttons = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Clear History", callback_data="clear_history"
                    )
                ],
                [InlineKeyboardButton(text="Settings AI", callback_data="ai_settings")],
            ]
        )

        for i in range(0, len(text), 4000):
            await message.answer(text[i : i + 4000], reply_markup=buttons)


# Clear User History
@router.callback_query(F.data == "clear_history")
async def clear_history_cb(callback: CallbackQuery, state: FSMContext):
    async with get_session() as session:
        user = await ensure_user(session, callback.from_user)

        await callback.message.edit_text("✅ History cleaned")
