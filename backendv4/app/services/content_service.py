from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from app.repositories.content_repository import ContentRepository
from app.schemas.content import ContentCreate


class ContentService:

    def __init__(self, db: Session):
        self.repo = ContentRepository(db)

    def clean_html(self, text: str | None):

        if not text:
            return ""

        return BeautifulSoup(text, "html.parser").get_text(" ", strip=True)

    def save_content(self, content: ContentCreate):

        # Check duplicate
        if self.repo.get_by_url(content.url):
            return None

        # Clean description
        cleaned_description = self.clean_html(content.description)

        # Build text for future embeddings
        content.content_text = f"{content.title} {cleaned_description}"

        content.description = cleaned_description

        return self.repo.create(content)