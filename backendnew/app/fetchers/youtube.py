import re
import feedparser
from datetime import datetime
from app.schemas.content import ContentCreate


YOUTUBE_CHANNELS = [
    {
        "name": "TED-Ed",
        "channel_id": "UCsooa4yRKGN_zEE8iknghZA",
        "category": "Education",
    },
    {
        "name": "Google for Developers",
        "channel_id": "UC_x5XG1OV2P6uZZ5FSM9Ttw",
        "category": "Technology",
    },
]


def _video_id(url: str):
    match = re.search(r"(?:watch\?v=|youtu\.be/|/shorts/)([A-Za-z0-9_-]{6,})", url or "")
    return match.group(1) if match else None


def _thumbnail(url: str):
    video_id = _video_id(url)
    return f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg" if video_id else None


def fetch_youtube(limit_per_channel: int = 15):
    videos = []

    for channel in YOUTUBE_CHANNELS:
        feed_url = (
            "https://www.youtube.com/feeds/videos.xml?channel_id="
            + channel["channel_id"]
        )
        parsed = feedparser.parse(feed_url)

        for entry in parsed.entries[:limit_per_channel]:
            url = entry.get("link", "").strip()
            title = entry.get("title", "").strip()

            if not url or not title:
                continue

            # RSS feeds expose normal videos reliably. If a source explicitly
            # identifies a Short, preserve it as SHORT instead of VIDEO.
            is_short = "/shorts/" in url or "#shorts" in title.lower()
            content_type = "short" if is_short else "video"

            videos.append(
                ContentCreate(
                    title=title,
                    description=entry.get("summary", ""),
                    content_type=content_type,
                    category=channel["category"],
                    source=channel["name"],
                    author=entry.get("author"),
                    url=url,
                    thumbnail=_thumbnail(url),
                    published_at=datetime.now(),
                )
            )

    return videos


def fetch_videos(limit_per_channel: int = 15):
    return [
        item for item in fetch_youtube(limit_per_channel)
        if item.content_type == "video"
    ]


def fetch_shorts(limit_per_channel: int = 30):
    return [
        item for item in fetch_youtube(limit_per_channel)
        if item.content_type == "short"
    ]
