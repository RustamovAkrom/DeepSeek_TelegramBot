from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, delete, func
from app.models.users import User
from typing import Optional, List


class CRUDUser:
    @staticmethod
    async def get_by_tg_id(session: AsyncSession, tg_id: int, load_history: bool = False) -> Optional[User]:
        q = select(User).where(User.tg_id == tg_id)
        if load_history:
            q = q.options(selectinload(User.histories))
        result = await session.execute(q)
        return result.scalars().first()
    
    @staticmethod
    async def count_users(session: AsyncSession) -> int:
        result = await session.execute(select(func.count()).select_from(User))
        return result.scalar() or 0
    
    @staticmethod
    async def delete_by_tg_id(session: AsyncSession, tg_id: int) -> bool:
        stmt = delete(User).where(User.tg_id == tg_id)
        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount > 0
        
    @staticmethod
    async def create(session: AsyncSession, **kwargs) -> User:
        user = User(**kwargs)
        session.add(user)
        await session.commit()
        await session.refresh(user, attribute_names=['histories'])
        return user
    
    @staticmethod
    async def update(session: AsyncSession, user: User, **kwargs) -> User:
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        session.add(user)
        await session.commit()
        await session.refresh(user, attribute_names=['histories'])
        return user

    @staticmethod
    async def list_users(session: AsyncSession, limit: int = 50, offset: int = 0, load_history: bool = False) -> List[User]:
        q = select(User).order_by(User.created_at.desc()).limit(limit).offset(offset)
        if load_history:
            q = q.options(selectinload(User.histories))
        result = await session.execute(q)
        return result.scalars().all()
