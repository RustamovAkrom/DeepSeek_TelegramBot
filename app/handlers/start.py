from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from app.db.base import AsyncSessionLocal
from app.services.user_service import ensure_user


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    async with AsyncSessionLocal() as session:
        user = await ensure_user(session, message.from_user)

    await message.answer("Welcome! You saved in the system.")
