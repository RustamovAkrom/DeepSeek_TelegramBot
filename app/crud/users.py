from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from app.models.users import User


class CRUDUser:
    @staticmethod
    async def get_by_tg_id(session: AsyncSession, tg_id: int):
        q = select(User).where(User.tg_id == tg_id)
        res = await session.execute(q)
        return res.scalars().first()
    
    @staticmethod
    async def count_users(session: AsyncSession) -> int:
        result = await session.execute(select(func.count()).select_from(User))
        return result.scalar() or 0
    
    @staticmethod
    async def delete_by_tg_id(session: AsyncSession, tg_id: int):
        stmt = delete(User).where(User.tg_id == tg_id)
        await session.execute(stmt)
        await session.commit()
        
    @staticmethod
    async def create(session: AsyncSession, **kwargs):
        user = User(**kwargs)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    
    @staticmethod
    async def update(session: AsyncSession, user: User, **kwargs):
        for k, v in kwargs.items():
            setattr(user, k, v)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def list_users(session: AsyncSession, limit: int = 50, offset: int = 0):
        q = select(User).order_by(User.created_at.desc()).limit(limit).offset(offset)
        res = await session.execute(q)
        return res.scalars().all()
    