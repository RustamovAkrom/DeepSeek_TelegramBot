from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from app.db.base import AsyncSessionLocal
from app.crud.users import CRUDUser
from config import settings

router = Router()

AVAILABLE_MODELS = settings.AVAILABLE_MODELS


def get_models_kb(current_model: str) -> InlineKeyboardMarkup:
    """Создаёт клавиатуру с моделями, отмечая текущую"""
    buttons = []
    for model in AVAILABLE_MODELS:
        text = f"{model} {'✅' if model == current_model else ''}"
        buttons.append(
            [InlineKeyboardButton(text=text, callback_data=f"set_model:{model}")]
        )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command("models"))
async def show_models(message: Message):
    """Показываем доступные модели через inline-кнопки"""
    async with AsyncSessionLocal() as session:
        user = await CRUDUser.get_by_tg_id(session, message.from_user.id)
        if not user:
            user = await CRUDUser.create(session, tg_id=message.from_user.id)
        current_model = user.get_model()

    kb = get_models_kb(current_model)
    await message.answer("Choose your model AI:", reply_markup=kb)


@router.callback_query(lambda c: c.data.startswith("set_model:"))
async def set_model(cb: CallbackQuery):
    display_name = cb.data.split(":")[1]  # "DeepSeek V3"
    model_id = settings.AVAILABLE_MODELS[
        display_name
    ]  # for example: "deepseek/deepseek-chat-v3-0324"

    async with AsyncSessionLocal() as session:
        user = await CRUDUser.get_by_tg_id(session, cb.from_user.id)
        await CRUDUser.update(
            session, user, meta={**(user.meta or {}), "default_model": model_id}
        )

    await cb.answer(f"Модель установлена: {display_name}", show_alert=True)
