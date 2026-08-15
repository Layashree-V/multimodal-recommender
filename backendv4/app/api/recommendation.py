from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.models.content import Content
from app.recommender.recommender import RecommendationEngine


router = APIRouter()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/recommend/{user_id}")
def recommend(
    user_id: int,
    content_type: str | None = Query(default=None),
    db: Session = Depends(get_db)
):

    engine = RecommendationEngine(db)

    results = engine.recommend(
        user_id
    )

    response = []

    for item in results:

        article = (
            db.query(Content)
            .filter(
                Content.id ==
                item["content_id"]
            )
            .first()
        )

        if article:
            if content_type and article.content_type.lower() != content_type.lower():
                continue

            response.append({

                "id": article.id,

                "title": article.title,

                "category": article.category,

                "source": article.source,

                "content_type": article.content_type,

                "description": article.description,

                "thumbnail": article.thumbnail,

                "url": article.url,

                "semantic_score":
                    item["semantic_score"],

                "category_score":
                    item["category_score"],

                "productivity_score":
                    item["productivity_score"],

                "diversity_penalty":
                    item["diversity_penalty"],

                "score":
                    item["score"]
            })

    return response