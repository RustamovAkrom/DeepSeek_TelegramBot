from sqlalchemy import Column, String, DateTime, ForeignKey, func, BigInteger
from sqlalchemy.orm import relationship
from app.db.base import BaseModel


class AIHistory(BaseModel):
    __tablename__ = "ai_histories"

    user_id = Column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="histories")

    def __repr__(self):
        return f"<{self.id} - User({self.user_id})>"
