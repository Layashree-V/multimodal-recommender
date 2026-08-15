from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text: str):

    if not text:
        text = ""

    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return [float(x) for x in embedding]