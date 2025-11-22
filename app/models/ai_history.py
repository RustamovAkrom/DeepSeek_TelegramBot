from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, BigInteger
from sqlalchemy.orm import relationship
from app.db.base import Base


class AIHistory(Base):
    __tablename__ = "ai_histories"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    role = Column(String, nullable=False)
    content = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="histories")

    def __repr__(self):
        return f"<{self.id} - User({self.user_id})>"
