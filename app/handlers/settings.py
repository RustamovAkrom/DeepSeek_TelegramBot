from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardButton, InlineKeyboardMarkup
)
from aiogram.fsm.context import FSMContext

from app.db.base import get_session
from app.services.user_service import ensure_user
from app.stats.settings_state import SettingsState


router = Router()


AVAILABLE_MODELS = [
    "deepseek-chat",
    "deepseek-reasoner",
    "deepseek-coder",
    "deepseek-r1",
    "deepseek-r1-lite",
    "deepseek-r1-distill",
]


def settings_menu(user_meta: dict):
    api_key = user_meta.get("api_key")
    model = user_meta.get("default_model")

    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"API Key: {'✅ Set' if api_key else '❌ Not set'}", callback_data="set_api_key")],
        [InlineKeyboardButton(text=f"Model: {model or 'default'}", callback_data="set_model")],
        [InlineKeyboardButton(text="❌ Remove API Key", callback_data="remove_api_key")],
    ])


@router.message(Command("settings"))
async def open_settings(message: Message, state: FSMContext):
    async with get_session() as session:
        user = await ensure_user(session, message.from_user)
        meta = user.meta or {}

        await message.answer(
            "⚙️ *AI Settings*",
            reply_markup=settings_menu(meta),
            parse_mode="Markdown"
        )


@router.callback_query(F.data == "set_api_key")
async def set_api_key_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsState.waiting_api_key)
    await callback.message.answer("🔑 Send me your *OpenRouter API Key*:")
    await callback.answer()


@router.message(SettingsState.waiting_api_key)
async def save_api_key(message: Message, state: FSMContext):
    api_key = message.text.strip()

    async with get_session() as session:
        user = await ensure_user(session, message.from_user)

        # initialize meta if missing
        if not user.meta:
            user.meta = {}

        user.meta["api_key"] = api_key

        session.add(user)
        await session.commit()

    await state.clear()
    await message.answer("✅ API Key saved!\nUse /settings again.")


@router.callback_query(F.data == "remove_api_key")
async def remove_api_key(callback: CallbackQuery):
    async with get_session() as session:
        user = await ensure_user(session, callback.from_user)
        if not user.meta:
            user.meta = {}

        user.meta.pop("api_key", None)
        session.add(user)
        await session.commit()

    await callback.message.edit_text("🗑 API Key removed.\nUse /settings again.")
    await callback.answer()


@router.callback_query(F.data == "set_model")
async def choose_model(callback: CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=model, callback_data=f"model:{model}")]
        for model in AVAILABLE_MODELS
    ])

    await callback.message.answer("🧠 Choose DeepSeek model:", reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("model:"))
async def set_model(callback: CallbackQuery):
    model_name = callback.data.split(":", 1)[1]

    async with get_session() as session:
        user = await ensure_user(session, callback.from_user)

        if not user.meta:
            user.meta = {}

        user.meta["default_model"] = model_name

        session.add(user)
        await session.commit()

    await callback.message.edit_text(f"✅ Model set: *{model_name}*", parse_mode="Markdown")
    await callback.answer()
