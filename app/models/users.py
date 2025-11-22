from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, func, BigInteger
from sqlalchemy.orm import relationship
from app.db.base import Base
import sqlalchemy as sa
from config import settings

JSONType = sa.JSON


class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    tg_id = Column(BigInteger, unique=True, index=True, nullable=False)
    token = Column(String, nullable=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    language_code = Column(String, nullable=True)
    is_bot = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    meta = Column(JSONType, nullable=True)

    histories = relationship(
        "AIHistory",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def get_api_key(self) -> str:
        meta = self.meta or {}
        return meta.get("api_key") or settings.DEEPSEEK_API_KEY

    def get_model(self) -> str:
        meta = self.meta or {}
        return meta.get("default_model") or settings.DEFAULT_MODEL

    def get_language(self) -> str:
        return self.meta["language"] if "language" in self.meta else "en"
        # if self.meta and "language" in self.meta:
        #     return self.meta['language']

        # if self.language_code:
        #     short = self.language_code[:2].lower()
        #     if short in ['en', 'ru', 'uz']:
        #         return short

        return "en"

    def __repr__(self):
        return f"<User tg_id={self.tg_id} username={self.username}>"
