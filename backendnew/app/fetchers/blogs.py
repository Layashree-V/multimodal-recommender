import feedparser
from datetime import datetime
from app.schemas.content import ContentCreate


BLOG_FEEDS = [
    {
        "name": "The Verge",
        "url": "https://www.theverge.com/rss/index.xml",
        "category": "Technology",
    },
    {
        "name": "Smashing Magazine",
        "url": "https://www.smashingmagazine.com/feed/",
        "category": "Technology",
    },
    {
        "name": "Nautilus",
        "url": "https://nautil.us/feed/",
        "category": "Science",
    },
]


def fetch_blogs(limit_per_feed: int = 20):
    blogs = []

    for feed in BLOG_FEEDS:
        parsed = feedparser.parse(feed["url"])

        for entry in parsed.entries[:limit_per_feed]:
            url = entry.get("link", "").strip()
            title = entry.get("title", "").strip()

            if not url or not title:
                continue

            blogs.append(
                ContentCreate(
                    title=title,
                    description=entry.get("summary", ""),
                    content_type="blog",
                    category=feed["category"],
                    source=feed["name"],
                    author=entry.get("author"),
                    url=url,
                    thumbnail=None,
                    published_at=datetime.now(),
                )
            )

    return blogs
