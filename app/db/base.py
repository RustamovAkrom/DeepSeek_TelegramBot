from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncIterator
from config import settings


DATABASE_URL = settings.current_database_url

engine = create_async_engine(
    DATABASE_URL, 
    echo=True,
    pool_pre_ping=True,
)

# 
AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Basic class for models
Base = declarative_base()

# Context manager
@asynccontextmanager
async def get_session():
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
