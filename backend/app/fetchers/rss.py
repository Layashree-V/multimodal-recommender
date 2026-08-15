import feedparser
from datetime import datetime

from app.schemas.content import ContentCreate


RSS_FEEDS = [
    {
        "name": "BBC Technology",
        "url": "https://feeds.bbci.co.uk/news/technology/rss.xml",
        "category": "Technology"
    },
    {
        "name": "NASA Breaking News",
        "url": "https://www.nasa.gov/rss/dyn/breaking_news.rss",
        "category": "Science"
    },
    {
        "name": "MIT News",
        "url": "https://news.mit.edu/rss/research",
        "category": "Research"
    }
]


def fetch_rss():

    articles = []

    for feed in RSS_FEEDS:

        parsed_feed = feedparser.parse(feed["url"])

        for entry in parsed_feed.entries:

            article = ContentCreate(

                title=entry.get("title", ""),

                description=entry.get("summary", ""),

                content_type="article",

                category=feed["category"],

                source=feed["name"],

                author=entry.get("author", None),

                url=entry.get("link", ""),

                thumbnail=None,

                published_at=datetime.now()

            )

            articles.append(article)

    return articles