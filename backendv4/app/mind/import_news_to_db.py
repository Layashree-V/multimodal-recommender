import pandas as pd

from app.mind.import_news import load_news
from app.database.connection import SessionLocal
from app.schemas.content import ContentCreate
from app.services.content_service import ContentService

# Create database session
db = SessionLocal()
service = ContentService(db)

# Load MIND dataset
df = load_news("datasets/MIND/news.tsv")

# Replace NaN values with empty strings
df = df.fillna("")

inserted = 0
skipped = 0

for _, row in df.iterrows():

    article = ContentCreate(
        title=row["title"],
        description=row["abstract"],
        content_type="article",
        content_text=row["abstract"],
        language="en",
        category=row["category"] if row["category"] else "General",
        source="MIND",
        author="Microsoft",
        url=row["url"] if row["url"] else f"mind://{row['news_id']}",
        thumbnail=None
    )

    result = service.save_content(article)

    if result:
        inserted += 1
    else:
        skipped += 1

    # Print progress every 1000 records
    if (inserted + skipped) % 1000 == 0:
        print(f"Processed: {inserted + skipped}")

print("\nImport Complete!")
print(f"Inserted: {inserted}")
print(f"Skipped: {skipped}")

db.close()