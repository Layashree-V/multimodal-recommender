from app.database.connection import SessionLocal
from app.embeddings.vector_store import VectorStore


def main():

    db = SessionLocal()

    store = VectorStore(db)

    store.build_index()

    db.close()


if __name__ == "__main__":
    main()