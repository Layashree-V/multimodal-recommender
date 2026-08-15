from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.embeddings.search import SemanticSearch
from app.models.content import Content

router = APIRouter()


def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/search")
def semantic_search(query: str, db: Session = Depends(get_db)):

    search = SemanticSearch()

    matches = search.search(query)

    response = []

    for match in matches:

        article = db.query(Content).filter(
            Content.id == match["content_id"]
        ).first()

        if article:

            response.append({

                "id": article.id,
                "title": article.title,
                "source": article.source,
                "category": article.category,
                "url": article.url,
                "content_type": article.content_type,
                "description": article.description,
                "thumbnail": article.thumbnail,
                "score": match["score"]

            })

    return response