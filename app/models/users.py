from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, func
from sqlalchemy.dialects.sqlite import JSON as SQLITE_JSON
from app.db.base import Base
import sqlalchemy as sa


JSONType = sa.JSON


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tg_id = Column(Integer, unique=True, index=True, nullable=False)
    token = Column(String, nullable=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    language_code = Column(String, nullable=True)
    is_bot = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    meta = Column(JSONType, nullable=True)
    ai_history = Column(JSONType, nullable=True, default=list)

    @property
    def get_ai_history(self) -> list:
        return self.ai_history or []
    
    def add_to_history(self, role: str, content: str, max_len: int = 5):
        """
        Добавляет сообщение в историю AI, ограничивая её max_len.
        """
        history = self.ai_history or []
        
        history.append({"role": role, "content": content})
        self.ai_history = history[-max_len:]

    def __repr__(self):
        return f"<User tg_id={self.tg_id} username={self.username}>"
