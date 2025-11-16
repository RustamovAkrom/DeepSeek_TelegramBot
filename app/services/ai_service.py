from typing import Optional, List, Dict
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User
from app.db.base import AsyncSessionLocal
from config import settings
import asyncio

class AIService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.DEEPSEEK_API_KEY
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1"
        )

    async def generate(
        self,
        user: User,
        text: str,
        model: Optional[str] = None,
        save_history: bool = True,
        session: Optional[AsyncSession] = None
) -> str:
        """
        Генерация ответа AI с сохранением истории пользователя.
        """
        model = model or user.meta.get("default_model") or settings.DEFAULT_MODEL
        api_key = user.meta.get("api_key") or settings.DEEPSEEK_API_KEY

        self.client.api_key = api_key
        # Берем только корректные элементы истории
        history = [
            msg for msg in (user.get_ai_history or [])
            if isinstance(msg, dict) and "role" in msg and "content" in msg
        ]

        messages = [
            {"role": "system", "content": "You are a helpful assistant. Continue conversation naturally."}
        ] + history + [
            {"role": "user", "content": text}  # здесь исправлено
        ]

        # Генерация ответа
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages
        )
        answer = response.choices[0].message.content

        # Обновляем историю
        if save_history:
            user.add_to_history("user", text)
            user.add_to_history("assistant", answer)
            if session:
                session.add(user)
                await session.commit()
                await session.refresh(user)

        return answer
