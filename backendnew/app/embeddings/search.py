import faiss
import pickle
import numpy as np

from app.embeddings.generator import generate_embedding


class SemanticSearch:

    def __init__(self):

        self.index = faiss.read_index("trained_models/content.index")

        with open("trained_models/id_mapping.pkl", "rb") as f:
            self.id_mapping = pickle.load(f)

    def search(self, query: str, top_k: int = 10):

        query_embedding = generate_embedding(query)

        query_embedding = np.array([query_embedding]).astype("float32")

        distances, indices = self.index.search(query_embedding, top_k)

        results = []

        for distance, index in zip(distances[0], indices[0]):

            if index == -1:
                continue

            results.append({
                "content_id": self.id_mapping[index],
                "distance": float(distance),
                "score": round(1 / (1 + float(distance)), 4)
            })

        return results