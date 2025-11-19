from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_session
from app.services.user_profile_service import UserProfileService
from app.services.user_service import ensure_user


router = Router()


@router.message(Command(commands=['history']))
async def show_profile(message: Message, state: FSMContext):
    async with get_session() as session:
        user = await ensure_user(session, message.from_user)
        profile = UserProfileService(user, session)

        history = profile.get_history()
        text = "🧾 Your History:\n\n" + "\n".join(
            [f"{i+1}. {item['role']}: {item['content']}" for i, item in enumerate(history)]
        )
        
        buttons = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Clear History", callback_data="clear_history")],
            [InlineKeyboardButton(text="Settings AI", callback_data="ai_settings")]
        ])
        
        await message.answer(text, reply_markup=buttons)


@router.callback_query(F.data == "clear_history")
async def clear_history_cb(callback: CallbackQuery, state: FSMContext):
    async with get_session() as session:
        user = await ensure_user(session, callback.from_user)
        profile = UserProfileService(user, session)
        await profile.clear_history()
        await callback.message.edit_text("✅ History cleaned")
