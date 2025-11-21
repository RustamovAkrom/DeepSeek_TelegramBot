from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.ai_history import AIHistory


class CRUDHistory:
    @staticmethod
    async def add(session: AsyncSession, user_id: int, role: str, content: str):
        obj = AIHistory(
            user_id=user_id,
            role=role,
            content=content
        )
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj
    
    @staticmethod
    async def list_user_history(session: AsyncSession, user_id: int, limit: int = 20):
        q = (
            select(AIHistory)
            .where(AIHistory.user_id == user_id)
            .order_by(AIHistory.created_at.asc())
            .limit(limit)
        )
        res = await session.execute(q)
        return res.scalars().all()
    
    @staticmethod
    async def clear(session: AsyncSession, user_id: int):
        stmt = delete(AIHistory).where(AIHistory.user_id == user_id)
        await session.execute(stmt)
        await session.commit()
