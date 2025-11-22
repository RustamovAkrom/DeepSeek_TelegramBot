from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, BigInteger
from typing import AsyncIterator
from config import settings
from typing import AsyncIterator


DATABASE_URL = settings.current_database_url

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
)

#
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    if settings.ENV == "prod":
        id = Column(BigInteger, primary_key=True, index=True)
    else:
        id = Column(Integer, primary_key=True, index=True, autoincrement=True)


# Context manager
@asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Import models
import app.models
