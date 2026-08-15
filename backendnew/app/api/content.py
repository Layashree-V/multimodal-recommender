from fastapi import APIRouter, Depends, HTTPException, Query
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


def serialize_content(item):
    return {
        "id": item.id,
        "title": item.title,
        "category": item.category,
        "source": item.source,
        "url": item.url,
        "description": item.description,
        "content_text": item.content_text,
        "content_type": item.content_type,
        "author": item.author,
        "thumbnail": item.thumbnail,
        "published_at": item.published_at,
        "score": 0.55,
    }


@router.get("/content/feed")
def content_feed(
    content_type: str | None = Query(default=None),
    limit: int = Query(default=24, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Latest content for a specific content type.

    Category pages use this instead of the personalized recommendation
    endpoint, so a new user can still see blogs, videos and shorts.
    """
    query = db.query(Content)

    if content_type:
        aliases = {
            "article": ["article", "articles", "news"],
            "blog": ["blog", "blogs"],
            "video": ["video", "videos"],
            "short": ["short", "shorts"],
        }
        values = aliases.get(
            content_type.lower(),
            [content_type.lower()],
        )
        query = query.filter(Content.content_type.in_(values))

    articles = (
        query
        .order_by(
            Content.published_at.desc().nullslast(),
            Content.fetched_at.desc(),
        )
        .limit(limit)
        .all()
    )

    return [serialize_content(item) for item in articles]


@router.get("/content/{content_id}")
def get_content(
    content_id: int,
    db: Session = Depends(get_db),
):
    article = (
        db.query(Content)
        .filter(Content.id == content_id)
        .first()
    )

    if not article:
        raise HTTPException(
            status_code=404,
            detail="Content not found",
        )

    return serialize_content(article)
