from app.database.connection import Base, engine

from app.models.user import User
from app.models.content import Content
from app.models.interaction import Interaction
from app.models.embedding import Embedding
#from app.models.bookmark import Bookmark
#from app.models.search_history import SearchHistory
#from app.models.recommendation import Recommendation


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_db()