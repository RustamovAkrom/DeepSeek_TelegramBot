from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.db.base import get_session
from app.services.user_service import ensure_user
from app.services.ai_service import AIService
from app.stats.chat_state import ChatState
from app.utils.base import split_text_for_telegram

import logging


router = Router()


@router.message(ChatState.waiting_for_ai)
async def wait_ai_response(message: Message):
    await message.answer("Plese wait, your promt generating...")


@router.message(F.text & ~F.command)
async def ai_chat(message: Message, state: FSMContext):
    """Generating AI response"""

    user_text = message.text.strip()
    if not user_text:
        await message.reply("Please write your prompt to generate AI response.")
        return

    await state.set_state(ChatState.waiting_for_ai)

    async with get_session() as session:
        user = await ensure_user(session, message.from_user)

        ai_service = AIService()

        try:
            response = await ai_service.generate(
                user=user,
                text=user_text, 
                save_history=True, 
                session=session
            )

        except Exception as e:
            logging.exception("Error generating AI response")
            await message.reply(f"Error in generating answer AI: {e}")
            await state.clear()
            return

    async for part in split_text_for_telegram(response):
        await message.reply(part)

    await state.clear()
