from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User
from app.services.user_service import ensure_user

class UserProfileService:
    def __init__(self, user: User, session: AsyncSession):
        self.user = user
        self.session = session

    def get_history(self, last: int = 10):
        return (self.user.get_ai_history or [])[-last:]

    async def clear_history(self):
        self.user.ai_history = []
        self.session.add(self.user)
        await self.session.commit()
        await self.session.refresh(self.user)

    async def delete_history_item(self, index: int):
        history = self.user.get_ai_history
        if 0 <= index < len(history):
            history.pop(index)
            self.user.ai_history = history
            self.session.add(self.user)
            await self.session.commit()
            await self.session.refresh(self.user)

    def get_settings(self):
        return self.user.meta or {}
    
    async def set_settings(self, key: str, value):
        meta = self.user.meta or {}
        meta[key] = value
        self.user.meta = meta
        self.session.add(self.user)
        await self.session.commit()
        await self.session.refresh(self.user)

    async def set_api_key(self, api_key: str):
        await self.set_settings("api_key", api_key)
    
    async def set_default_model(self, model: str):
        await self.set_settings("default_model", model)
