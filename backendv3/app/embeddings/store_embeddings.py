from app.database.connection import SessionLocal
from app.models.content import Content
from app.models.embedding import Embedding
from app.embeddings.generator import generate_embedding

db = SessionLocal()

contents = db.query(Content).all()

inserted = 0
updated = 0

print(f"Generating embeddings for {len(contents)} articles...\n")

for item in contents:

    text = f"""
{item.title or ""}

{item.description or ""}

{item.content_text or ""}
"""

    # Generate embedding
    vector = generate_embedding(text)

    # Convert numpy.float32 -> Python float
    vector = [float(x) for x in vector]

    existing = (
        db.query(Embedding)
        .filter(Embedding.content_id == item.id)
        .first()
    )

    if existing:
        existing.vector = vector
        updated += 1
    else:
        db.add(
            Embedding(
                content_id=item.id,
                vector=vector
            )
        )
        inserted += 1

    item.embedding_generated = True

    if (inserted + updated) % 100 == 0:
        db.commit()
        print(f"{inserted + updated}/{len(contents)} completed")

db.commit()

print("\n==============================")
print(f"Inserted : {inserted}")
print(f"Updated  : {updated}")
print("Embedding generation completed.")
print("==============================")

db.close()