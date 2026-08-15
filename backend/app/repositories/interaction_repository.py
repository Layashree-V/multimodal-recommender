from app.models.interaction import Interaction

class InteractionRepository:

    def __init__(self, db):
        self.db = db

    def create(self, interaction):

        self.db.add(interaction)
        self.db.commit()
        self.db.refresh(interaction)

        return interaction