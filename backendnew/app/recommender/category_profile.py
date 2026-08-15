from collections import defaultdict

from app.models.interaction import Interaction
from app.models.content import Content


class CategoryPreferenceBuilder:

    def __init__(self, db):
        self.db = db

    def build_preferences(self, user_id: int):

        interactions = (
            self.db.query(Interaction, Content)
            .join(
                Content,
                Interaction.content_id == Content.id
            )
            .filter(
                Interaction.user_id == user_id
            )
            .all()
        )

        category_scores = defaultdict(float)

        for interaction, content in interactions:

            if not content.category:
                continue

            weight = 1.0

            if interaction.clicked:
                weight += 1.0

            if interaction.liked:
                weight += 3.0

            if interaction.saved:
                weight += 4.0

            if interaction.shared:
                weight += 5.0

            if interaction.watch_time:
                weight += min(
                    interaction.watch_time / 60.0,
                    3.0
                )

            if interaction.read_time:
                weight += min(
                    interaction.read_time / 60.0,
                    3.0
                )

            category_scores[content.category] += weight

        if not category_scores:
            return {}

        total = sum(category_scores.values())

        preferences = {
            category: score / total
            for category, score
            in category_scores.items()
        }

        return preferences