from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.models.content import Content

router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/content/{content_id}")
def get_content(
    content_id: int,
    db: Session = Depends(get_db)
):
    article = (
        db.query(Content)
        .filter(Content.id == content_id)
        .first()
    )

    if not article:
        raise HTTPException(
            status_code=404,
            detail="Content not found"
        )

    return {
        "id": article.id,
        "title": article.title,
        "category": article.category,
        "source": article.source,
        "url": article.url,
        "description": article.description,
        "content_text": article.content_text
    }