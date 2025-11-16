from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import users as crud_users
from app.models.users import User
from aiogram.types import User as TgUser


async def ensure_user(session: AsyncSession, tg_user: TgUser) -> User:
    """Создаёт или обновляет пользователя в БД."""
    existing = await crud_users.CRUDUser.get_by_tg_id(session, tg_user.id)
    data = {
        "tg_id": tg_user.id,
        "username": getattr(tg_user, "username", None),
        "first_name": getattr(tg_user, "first_name", None),
        "last_name": getattr(tg_user, "last_name", None),
        "language_code": getattr(tg_user, "language_code", None),
        "is_bot": getattr(tg_user, "is_bot", False),
    }
    if existing is None:
        user = await crud_users.CRUDUser.create(session, **data)
        return user
    else:
        user = await crud_users.CRUDUser.update(session, existing, **data)
        return user
