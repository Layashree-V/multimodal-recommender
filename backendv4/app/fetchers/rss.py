import feedparser
from datetime import datetime

from app.schemas.content import ContentCreate


RSS_FEEDS = [
    {"name": "BBC Technology", "url": "https://feeds.bbci.co.uk/news/technology/rss.xml", "category": "Technology"},
    {"name": "NASA Breaking News", "url": "https://www.nasa.gov/rss/dyn/breaking_news.rss", "category": "Science"},
    {"name": "MIT News", "url": "https://news.mit.edu/rss/research", "category": "Research"},
    {"name": "ESPN News", "url": "https://www.espn.com/espn/rss/news", "category": "Sports"},
    {"name": "CNBC Business", "url": "https://www.cnbc.com/id/100003114/device/rss/rss.html", "category": "Business"},
    {"name": "BBC Travel", "url": "https://feeds.bbci.co.uk/news/world/rss.xml", "category": "Travel"},
    {"name": "NPR Education", "url": "https://feeds.npr.org/1013/rss.xml", "category": "Education"},
    {"name": "BBC Entertainment", "url": "https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml", "category": "Entertainment"},
    {"name": "BBC World", "url": "https://feeds.bbci.co.uk/news/world/rss.xml", "category": "News"},
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