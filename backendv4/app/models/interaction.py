from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    Float,
    ForeignKey,
    DateTime,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    content_id = Column(
        Integer,
        ForeignKey("content.id"),
        nullable=False,
        index=True
    )

    clicked = Column(
        Boolean,
        default=False
    )

    liked = Column(
        Boolean,
        default=False
    )

    saved = Column(
        Boolean,
        default=False
    )

    shared = Column(
        Boolean,
        default=False
    )

    watch_time = Column(
        Float,
        default=0
    )

    read_time = Column(
        Float,
        default=0
    )

    scroll_depth = Column(
        Float,
        default=0
    )

    interaction_time = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationship with User
    user = relationship(
        "User",
        back_populates="interactions"
    )

    # Relationship with Content
    content = relationship(
        "Content",
        back_populates="interactions"
    )