from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Embedding(Base):

    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True, index=True)

    content_id = Column(
        Integer,
        ForeignKey("content.id"),
        unique=True,
        nullable=False
    )

    vector = Column(
        ARRAY(Float),
        nullable=False
    )

    content = relationship(
        "Content",
        back_populates="embedding"
    )