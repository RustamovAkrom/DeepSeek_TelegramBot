from typing import Optional
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User
from config import settings


class AIService:
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        base_url: Optional[str] = None
    ):
        self.api_key = api_key or settings.DEEPSEEK_API_KEY

        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=base_url or settings.BASE_URL,
            # default_headers={
            #     "HTTP-Referer": "https://yourdomain.com",
            #     "X-Title": "AiogramBot"
            # }
        )
    

    async def generate(
        self,
        user: User,
        text: str,
        model: Optional[str] = None,
        save_history: bool = True,
        session: Optional[AsyncSession] = None
    ) -> str:

        # НЕ затираем meta
        model = model or user.get_model()
        
        # История диалога
        history = [
            msg for msg in (user.get_ai_history or [])
            if isinstance(msg, dict) and "role" in msg and "content" in msg
        ]

        messages = (
            [{"role": "system", "content": "You are a helpful assistant."}]
            + history
            + [{"role": "user", "content": text}]
        )

        # -------------------------
        # ВАЖНО: новый метод вызова
        # -------------------------
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
        )

        answer = response.choices[0].message.content

        if save_history:
            user.add_to_history("user", text)
            user.add_to_history("assistant", answer)

            if session:
                session.add(user)
                await session.commit()
                await session.refresh(user)
                

        return answer
