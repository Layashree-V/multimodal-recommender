import re
import feedparser
from datetime import datetime
from app.schemas.content import ContentCreate


# A diverse set of public YouTube channels.  RSS is used instead of the
# YouTube Data API, so no API key is required.
YOUTUBE_CHANNELS = [
    {"name": "TED-Ed", "channel_id": "UCsooa4yRKGN_zEE8iknghZA", "category": "Education"},
    {"name": "Google for Developers", "channel_id": "UC_x5XG1OV2P6uZZ5FSM9Ttw", "category": "Technology"},
    {"name": "freeCodeCamp.org", "channel_id": "UC8butISFwT-Wl7EV0hUK0BQ", "category": "Technology"},
    {"name": "Fireship", "channel_id": "UCsBjURrPoezykLs9EqgamOA", "category": "Technology"},
    {"name": "WIRED", "channel_id": "UCsT0YIqwnpJCM-mx7-gSA4Q", "category": "Technology"},
    {"name": "BBC News", "channel_id": "UC16niRr50-MSBwiO3YDb3RA", "category": "News"},
    {"name": "CNBC", "channel_id": "UCvJJ_dzjViJCoLf5uKUTwoA", "category": "Business"},
    {"name": "National Geographic", "channel_id": "UCpVm7bg6pXKo1Pr6k5kxG9A", "category": "Science"},
    {"name": "Veritasium", "channel_id": "UCHnyfMqiRRG1u-2MsSQLbXA", "category": "Science"},
    {"name": "Kurzgesagt – In a Nutshell", "channel_id": "UCsXVk37bltHxD1rDPwtNM8Q", "category": "Science"},
]


def _video_id(url: str):
    match = re.search(r"(?:watch\?v=|youtu\.be/|/shorts/)([A-Za-z0-9_-]{6,})", url or "")
    return match.group(1) if match else None


def _thumbnail(url: str):
    video_id = _video_id(url)
    return f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg" if video_id else None


def fetch_youtube(limit_per_channel: int = 8):
    videos = []

    for channel in YOUTUBE_CHANNELS:
        feed_url = "https://www.youtube.com/feeds/videos.xml?channel_id=" + channel["channel_id"]
        parsed = feedparser.parse(feed_url)

        for entry in parsed.entries[:limit_per_channel]:
            url = entry.get("link", "").strip()
            title = entry.get("title", "").strip()
            if not url or not title:
                continue

            # YouTube RSS normally returns /watch URLs.  Preserve Shorts when
            # the feed explicitly marks them; regular entries remain videos.
            lower_title = title.lower()
            is_short = "/shorts/" in url or "#shorts" in lower_title or " #short" in lower_title
            content_type = "short" if is_short else "video"

            videos.append(ContentCreate(
                title=title,
                description=entry.get("summary", ""),
                content_type=content_type,
                category=channel["category"],
                source=channel["name"],
                author=entry.get("author"),
                url=url,
                thumbnail=_thumbnail(url),
                published_at=datetime.now(),
            ))

    return videos


def fetch_videos(limit_per_channel: int = 8):
    return [item for item in fetch_youtube(limit_per_channel) if item.content_type == "video"]


def fetch_shorts(limit_per_channel: int = 30):
    return [item for item in fetch_youtube(limit_per_channel) if item.content_type == "short"]
