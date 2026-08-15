from app.database.connection import SessionLocal
from app.fetchers.rss import fetch_rss
from app.fetchers.blogs import fetch_blogs
from app.fetchers.youtube import fetch_youtube
from app.services.content_service import ContentService


def ingest_items(service, label, items):
    inserted = 0
    skipped = 0

    print(f"\nFetching {label}...")
    print(f"Fetched {len(items)} {label}")

    for item in items:
        result = service.save_content(item)
        if result:
            inserted += 1
        else:
            skipped += 1

    print(f"{label} -> inserted: {inserted}, skipped: {skipped}")
    return inserted, skipped


def main():
    db = SessionLocal()
    service = ContentService(db)

    try:
        ingest_items(service, "articles", fetch_rss())
        ingest_items(service, "blogs", fetch_blogs())
        ingest_items(service, "videos/shorts", fetch_youtube())
    finally:
        db.close()

    print("\nContent ingestion complete.")


if __name__ == "__main__":
    main()
