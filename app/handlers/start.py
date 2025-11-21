from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from app.db.base import get_session
from app.services.user_service import ensure_user


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    async with get_session() as session:
        user = await ensure_user(session, message.from_user)

    await message.answer(f"Welcome {user.first_name}! You saved in the system.")
