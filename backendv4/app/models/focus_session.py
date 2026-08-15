from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.connection import Base


class FocusSession(Base):
    __tablename__ = "focus_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    goal = Column(String(500), nullable=False, default="General learning")
    duration_minutes = Column(Float, nullable=False, default=20)
    elapsed_seconds = Column(Float, nullable=False, default=0)

    status = Column(String(30), nullable=False, default="active")
    content_ids = Column(Text, nullable=False, default="[]")

    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="focus_sessions")
