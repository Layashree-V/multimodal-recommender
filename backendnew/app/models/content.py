from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(500), nullable=False)

    description = Column(Text)

    content_type = Column(String(50), nullable=False)

    content_text = Column(Text)

    language = Column(String(20), default="en")

    category = Column(String(100))

    source = Column(String(100))

    author = Column(String(255))

    url = Column(Text, unique=True, nullable=False)

    thumbnail = Column(Text)

    published_at = Column(DateTime(timezone=True))

    fetched_at = Column(DateTime(timezone=True),
                        server_default=func.now())

    embedding_generated = Column(Boolean, default=False)

    interactions = relationship(
        "Interaction",
        back_populates="content",
        cascade="all, delete-orphan"
    )

    embedding = relationship(
    "Embedding",
    back_populates="content",
    uselist=False
)