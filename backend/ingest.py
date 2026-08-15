from app.database.connection import SessionLocal
from app.fetchers.rss import fetch_rss
from app.services.content_service import ContentService


def main():

    db = SessionLocal()

    service = ContentService(db)

    print("Fetching RSS articles...")

    articles = fetch_rss()

    print(f"Fetched {len(articles)} articles")

    inserted = 0
    skipped = 0

    for article in articles:

        result = service.save_content(article)

        if result:
            inserted += 1
        else:
            skipped += 1

    db.close()

    print(f"\nInserted : {inserted}")
    print(f"Skipped  : {skipped}")


if __name__ == "__main__":
    main()