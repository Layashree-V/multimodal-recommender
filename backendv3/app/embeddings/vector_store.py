import faiss
import numpy as np
import pickle

from sqlalchemy.orm import Session

from app.models.content import Content
from app.embeddings.generator import generate_embedding


class VectorStore:

    def __init__(self, db: Session):
        self.db = db

    def build_index(self):

        # Fetch all content from database
        contents = self.db.query(Content).all()

        print(f"Found {len(contents)} articles.\n")

        embeddings = []
        id_mapping = []

        for i, item in enumerate(contents, start=1):

            # Skip articles without content
            if not item.content_text:
                continue

            # Combine title + description + content
            text = f"""
{item.title or ""}

{item.description or ""}

{item.content_text or ""}
"""

            # Generate embedding
            embedding = generate_embedding(text)

            embeddings.append(embedding)
            id_mapping.append(item.id)

            # Show progress every 500 articles
            if i % 500 == 0:
                print(f"Processed {i}/{len(contents)} articles")

        # Safety check
        if len(embeddings) == 0:
            print("No embeddings generated.")
            return

        print("\nConverting embeddings to NumPy array...")

        embeddings = np.array(embeddings).astype("float32")

        dimension = embeddings.shape[1]

        print(f"Embedding dimension: {dimension}")

        print("\nBuilding FAISS index...")

        # Cosine similarity (works with normalized embeddings)
        index = faiss.IndexFlatIP(dimension)

        index.add(embeddings)

        print("Saving FAISS index...")

        faiss.write_index(
            index,
            "trained_models/content.index"
        )

        print("Saving ID mapping...")

        with open(
            "trained_models/id_mapping.pkl",
            "wb"
        ) as f:
            pickle.dump(id_mapping, f)

        print("\n====================================")
        print("Vector database created successfully!")
        print(f"Indexed Articles : {len(id_mapping)}")
        print("FAISS Index      : trained_models/content.index")
        print("ID Mapping       : trained_models/id_mapping.pkl")
        print("====================================")