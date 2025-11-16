from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncIterator
from config import settings


DATABASE_URL = settings.DATABASE_URL if settings.ENV == "prod" else settings.TEST_DATABASE_URL or settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=settings.ENV=="dev")
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


@asynccontextmanager
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
