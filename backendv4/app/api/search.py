from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

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


def serialize(article, score=0.0):
    return {
        "id": article.id,
        "title": article.title,
        "source": article.source,
        "category": article.category,
        "url": article.url,
        "content_type": article.content_type,
        "description": article.description,
        "thumbnail": article.thumbnail,
        "score": round(float(score), 4),
    }


CATEGORY_ALIASES = {
    "sports": ["sports", "sport", "football", "soccer", "basketball", "tennis", "cricket"],
    "technology": ["technology", "tech", "software", "gadgets", "developers", "programming"],
    "science": ["science", "research", "ai", "space", "nasa"],
    "business": ["business", "finance", "markets", "economy", "money", "startup", "startups"],
    "travel": ["travel", "tourism", "destinations", "airlines", "hotels"],
    "news": ["news", "world", "politics", "current events"],
    "education": ["education", "learning", "school", "university", "students"],
    "entertainment": ["entertainment", "gaming", "games", "movies", "music", "tv"],
}


def lexical_search(db: Session, query: str, limit: int = 20):
    raw = query.strip().lower()
    terms = [t for t in raw.replace("-", " ").split() if len(t) > 1]
    expanded = []
    for term in terms:
        expanded.extend(CATEGORY_ALIASES.get(term, [term]))
    terms = list(dict.fromkeys(expanded))

    if not terms:
        return []

    conditions = []
    for term in terms:
        pattern = f"%{term}%"
        conditions.extend([
            Content.title.ilike(pattern),
            Content.description.ilike(pattern),
            Content.category.ilike(pattern),
            Content.source.ilike(pattern),
            Content.content_text.ilike(pattern),
        ])

    matches = (
        db.query(Content)
        .filter(or_(*conditions))
        .order_by(Content.published_at.desc().nullslast(), Content.fetched_at.desc())
        .limit(limit)
        .all()
    )
    return [serialize(item, 0.5) for item in matches]


@router.get("/search")
def semantic_search(query: str, db: Session = Depends(get_db)):
    value = query.strip()
    if not value:
        return []

    # Semantic search is preferred, but the FAISS index can lag behind newly
    # ingested RSS/blog/video content. Always supplement it with DB text search.
    response = []
    try:
        search = SemanticSearch()
        matches = search.search(value, top_k=20)
        seen = set()
        for match in matches:
            article = db.query(Content).filter(Content.id == match["content_id"]).first()
            if article and article.id not in seen:
                response.append(serialize(article, match.get("score", 0.0)))
                seen.add(article.id)
    except Exception:
        # Search should still work when the optional vector index is unavailable.
        pass

    lexical = lexical_search(db, value, limit=20)
    for item in lexical:
        if item["id"] not in {r["id"] for r in response}:
            response.append(item)

    return response[:20]
