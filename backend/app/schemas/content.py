from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ContentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    content_text: Optional[str] = None

    content_type: str
    category: Optional[str] = None

    source: str
    author: Optional[str] = None

    url: str
    thumbnail: Optional[str] = None

    language: str = "en"

    published_at: Optional[datetime] = None