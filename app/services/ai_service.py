from typing import Optional
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User
from app.crud.history import CRUDHistory


from config import settings


class AIService:
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        base_url: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        top_p: float = 1.0,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        system_prompt: str = "You are a helpful assistant."
    ):
        self.api_key = api_key or settings.DEEPSEEK_API_KEY
        self.base_url = base_url or settings.BASE_URL
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.system_prompt = system_prompt

        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    

    async def generate(
        self,
        user: User,
        text: str,
        model: Optional[str] = None,
        save_history: bool = True,
        session: Optional[AsyncSession] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        system_prompt: Optional[str] = None,
    ) -> str:

        if session is None:
            raise ValueError("AsyncSession is required to save/retrieve history.")

        # Getting Model
        model = model or user.get_model()

        # Settings params
        max_tokens = min(max_tokens or self.max_tokens, 16000)  # безопасный лимит для free
        temperature = temperature if temperature is not None else self.temperature
        top_p = top_p if top_p is not None else self.top_p
        presence_penalty = presence_penalty if presence_penalty is not None else self.presence_penalty
        frequency_penalty = frequency_penalty if frequency_penalty is not None else self.frequency_penalty
        system_prompt = system_prompt or self.system_prompt
        
        # History
        history_objs = await CRUDHistory.list_user_history(
            session, 
            user_id=user.id,
            limit=settings.MAX_HISTORY
        )
        history = [{"role": h.role, "content": h.content} for h in history_objs]

        # Formatting History
        messages = [{"role": "system", "content": system_prompt}]
        messages += history
        messages.append({"role": "user", "content": text})
        
        try:
            # Generating response of AI
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty
            )
        except Exception as e:
            raise RuntimeError(f"AI generation error: {e}")
        
        # Response
        answer = response.choices[0].message.content

        if save_history:
            # User request
            await CRUDHistory.add( session=session, user_id=user.id, role="user", content=text )
            # AI response
            await CRUDHistory.add( session=session, user_id=user.id, role="assistant", content=answer )

        return answer

    async def set_user_model(self, session: AsyncSession, user: User, model_name: str):
        meta = user.meta or {}
        meta['default_model'] = model_name
        user.meta = meta
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    
    async def get_user_model(self, user: User) -> str:
        return user.get_model()
