from sqlalchemy.orm import Session

from app.models.content import Content
from app.schemas.content import ContentCreate


class ContentRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_url(self, url: str):
        return self.db.query(Content).filter(Content.url == url).first()

    def create(self, content: ContentCreate):

        db_content = Content(
            title=content.title,
            description=content.description,
            content_text=content.content_text,
            content_type=content.content_type,
            category=content.category,
            source=content.source,
            author=content.author,
            url=content.url,
            thumbnail=content.thumbnail,
            language=content.language,
            published_at=content.published_at
        )

        self.db.add(db_content)
        self.db.commit()
        self.db.refresh(db_content)

        return db_content