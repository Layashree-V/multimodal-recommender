from collections import defaultdict
from datetime import datetime, timedelta, timezone

from app.models.interaction import Interaction
from app.models.content import Content


class InterestDetector:

    def __init__(self, db):
        self.db = db

    def detect_interest_change(
        self,
        user_id: int,
        recent_days: int = 7
    ):
        """
        Compare the user's recent category interest
        with their historical category interest.

        Returns:
        {
            "category": {
                "recent_score": ...,
                "historical_score": ...,
                "change": ...,
                "trend": ...
            }
        }
        """

        # -------------------------------------------------
        # 1. Get all user interactions
        # -------------------------------------------------

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

        if not interactions:
            return {}

        # -------------------------------------------------
        # 2. Current time
        # -------------------------------------------------

        now = datetime.now(timezone.utc)

        recent_cutoff = (
            now - timedelta(days=recent_days)
        )

        # -------------------------------------------------
        # 3. Category scores
        # -------------------------------------------------

        recent_scores = defaultdict(float)
        historical_scores = defaultdict(float)

        # -------------------------------------------------
        # 4. Calculate interaction weight
        # -------------------------------------------------

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

            # -------------------------------------------------
            # 5. Separate recent and historical interactions
            # -------------------------------------------------

            interaction_time = (
                interaction.interaction_time
            )

            if interaction_time is None:
                historical_scores[
                    content.category
                ] += weight

                continue

            # SQLAlchemy may return a timezone-naive datetime
            if interaction_time.tzinfo is None:
                interaction_time = interaction_time.replace(
                    tzinfo=timezone.utc
                )

            if interaction_time >= recent_cutoff:

                recent_scores[
                    content.category
                ] += weight

            else:

                historical_scores[
                    content.category
                ] += weight

        # -------------------------------------------------
        # 6. Normalize scores
        # -------------------------------------------------

        recent_total = sum(
            recent_scores.values()
        )

        historical_total = sum(
            historical_scores.values()
        )

        # -------------------------------------------------
        # If there is no historical data,
        # use recent data as the current profile
        # -------------------------------------------------

        if historical_total == 0:

            return {
                category: {
                    "recent_score": round(
                        score / recent_total,
                        4
                    ) if recent_total else 0.0,

                    "historical_score": 0.0,

                    "change": round(
                        score / recent_total,
                        4
                    ) if recent_total else 0.0,

                    "trend": "new"
                }

                for category, score
                in recent_scores.items()
            }

        # -------------------------------------------------
        # 7. Get all categories
        # -------------------------------------------------

        categories = set(
            recent_scores.keys()
        ).union(
            historical_scores.keys()
        )

        # -------------------------------------------------
        # 8. Calculate interest change
        # -------------------------------------------------

        results = {}

        for category in categories:

            recent_score = (
                recent_scores.get(
                    category,
                    0.0
                ) / recent_total
                if recent_total
                else 0.0
            )

            historical_score = (
                historical_scores.get(
                    category,
                    0.0
                ) / historical_total
                if historical_total
                else 0.0
            )

            change = (
                recent_score
                - historical_score
            )

            # -------------------------------------------------
            # Determine trend
            # -------------------------------------------------

            if change >= 0.15:

                trend = "increasing"

            elif change <= -0.15:

                trend = "decreasing"

            else:

                trend = "stable"

            results[category] = {

                "recent_score": round(
                    recent_score,
                    4
                ),

                "historical_score": round(
                    historical_score,
                    4
                ),

                "change": round(
                    change,
                    4
                ),

                "trend": trend
            }

        # -------------------------------------------------
        # 9. Sort by strongest change
        # -------------------------------------------------

        results = dict(
            sorted(
                results.items(),
                key=lambda item: abs(
                    item[1]["change"]
                ),
                reverse=True
            )
        )

        return results