from app.database.connection import SessionLocal
from app.embeddings.vector_store import VectorStore

db = SessionLocal()

store = VectorStore(db)
store.build_index()

db.close()