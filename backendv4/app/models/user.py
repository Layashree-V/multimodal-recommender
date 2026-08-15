from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.connection import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    password = Column(
        String(255),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    interactions = relationship(
        "Interaction",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    focus_sessions = relationship(
        "FocusSession",
        back_populates="user",
        cascade="all, delete-orphan"
    )