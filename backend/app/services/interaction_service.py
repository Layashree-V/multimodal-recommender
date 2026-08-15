from app.models.interaction import Interaction
from app.repositories.interaction_repository import InteractionRepository


class InteractionService:

    def __init__(self, db):
        self.repo = InteractionRepository(db)

    def save(self, data):

        interaction = Interaction(
            user_id=data.user_id,
            content_id=data.content_id,

            clicked=data.clicked,
            liked=data.liked,
            saved=data.saved,
            shared=data.shared,

            watch_time=data.watch_time,
            read_time=data.read_time,
            scroll_depth=data.scroll_depth
        )

        return self.repo.create(interaction)