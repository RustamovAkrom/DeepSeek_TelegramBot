from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import users as crud_users
from app.models.users import User
from aiogram.types import User as TgUser


async def ensure_user(session: AsyncSession, tg_user: TgUser) -> User:
    existing = await crud_users.CRUDUser.get_by_tg_id(session, tg_user.id)

    data = {
        "tg_id": tg_user.id,
        "username": tg_user.username,
        "first_name": tg_user.first_name,
        "last_name": tg_user.last_name,
        "language_code": tg_user.language_code,
        "is_bot": tg_user.is_bot,
    }
    if existing is None:
        user = await crud_users.CRUDUser.create(session, **data)
        return user
    else:
        user = await crud_users.CRUDUser.update(session, existing, **data)
        return user
