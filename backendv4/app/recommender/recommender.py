import os
import faiss
import pickle
import numpy as np

from app.recommender.profile_builder import UserProfileBuilder
from app.recommender.category_profile import CategoryPreferenceBuilder
from app.classifier.productivity_classifier import ProductivityClassifier
from app.recommender.ranking_model import RankingModel
from app.recommender.interest_detector import InterestDetector

from app.models.interaction import Interaction
from app.models.content import Content


class RecommendationEngine:

    def __init__(self, db):

        self.db = db

        # =========================================
        # USER PROFILE
        # =========================================

        self.profile_builder = UserProfileBuilder(db)

        # =========================================
        # CATEGORY PREFERENCES
        # =========================================

        self.category_builder = CategoryPreferenceBuilder(db)

        # =========================================
        # PRODUCTIVITY CLASSIFIER
        # =========================================

        self.productivity_classifier = (
            ProductivityClassifier()
        )

        # =========================================
        # INTEREST CHANGE DETECTOR
        # =========================================

        self.interest_detector = (
            InterestDetector(db)
        )

        # =========================================
        # RANKING MODEL
        # =========================================

        self.ranking_model = RankingModel()

        # =========================================
        # LOAD FAISS INDEX
        # =========================================

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
        )

        self.models_dir = os.path.join(
            base_dir,
            "trained_models"
        )

        self.index_path = os.path.join(
            self.models_dir,
            "content.index"
        )

        self.mapping_path = os.path.join(
            self.models_dir,
            "id_mapping.pkl"
        )

        self.index = faiss.read_index(
            self.index_path
        )

        # =========================================
        # LOAD FAISS ID MAPPING
        # =========================================

        with open(
            self.mapping_path,
            "rb"
        ) as f:

            self.id_mapping = pickle.load(f)

    # =====================================================
    # GET INTEREST TREND BOOST
    # =====================================================

    def get_interest_boost(
        self,
        category,
        interest_changes
    ):

        if not interest_changes:
            return 0.0

        interest = interest_changes.get(
            category
        )

        if not interest:
            return 0.0

        trend = interest.get(
            "trend",
            "stable"
        )

        # -----------------------------------------
        # New interest
        # -----------------------------------------

        if trend == "new":

            return 0.05

        # -----------------------------------------
        # Increasing interest
        # -----------------------------------------

        elif trend == "increasing":

            return 0.08

        # -----------------------------------------
        # Stable interest
        # -----------------------------------------

        elif trend == "stable":

            return 0.0

        # -----------------------------------------
        # Decreasing interest
        # -----------------------------------------

        elif trend == "decreasing":

            return -0.05

        return 0.0

    # =====================================================
    # NORMALIZE RANKING SCORES
    # =====================================================

    def normalize_ranking_scores(
        self,
        candidates
    ):

        if not candidates:
            return candidates

        scores = np.array(
            [
                candidate["raw_ranking_score"]
                for candidate in candidates
            ],
            dtype=np.float32
        )

        minimum = float(
            np.min(scores)
        )

        maximum = float(
            np.max(scores)
        )

        # -----------------------------------------
        # All predictions identical
        # -----------------------------------------

        if maximum == minimum:

            for candidate in candidates:

                candidate["ranking_score"] = 0.5

            return candidates

        # -----------------------------------------
        # Min-Max normalization
        # -----------------------------------------

        for candidate in candidates:

            raw_score = (
                candidate["raw_ranking_score"]
            )

            normalized_score = (
                (raw_score - minimum)
                / (maximum - minimum)
            )

            candidate["ranking_score"] = round(
                float(normalized_score),
                4
            )

        return candidates

    # =====================================================
    # RECOMMEND
    # =====================================================

    def recommend(
        self,
        user_id: int,
        top_k: int = 10
    ):

        # =========================================
        # 1. BUILD USER PROFILE
        # =========================================

        user_vector = (
            self.profile_builder
            .build_profile(user_id)
        )

        if user_vector is None:

            return []

        query = np.array(
            [user_vector],
            dtype="float32"
        )

        # =========================================
        # 2. RETRIEVE CANDIDATES FROM FAISS
        # =========================================

        search_k = self.index.ntotal

        if search_k <= 0:

            return []

        distances, indices = (
            self.index.search(
                query,
                search_k
            )
        )

        # =========================================
        # 3. GET CONSUMED CONTENT
        # =========================================

        interactions = (
            self.db.query(
                Interaction.content_id
            )
            .filter(
                Interaction.user_id == user_id
            )
            .all()
        )

        consumed_ids = {
            item[0]
            for item in interactions
        }

        # =========================================
        # 4. CATEGORY PREFERENCES
        # =========================================

        category_preferences = (
            self.category_builder
            .build_preferences(user_id)
        )

        print(
            "CATEGORY PREFERENCES:"
        )

        print(
            category_preferences
        )

        # =========================================
        # 5. INTEREST CHANGE DETECTION
        # =========================================

        interest_changes = (
            self.interest_detector
            .detect_interest_change(
                user_id
            )
        )

        print(
            "INTEREST CHANGES:"
        )

        print(
            interest_changes
        )

        # =========================================
        # 6. HISTORICAL USER ENGAGEMENT
        # =========================================

        user_interactions = (
            self.db.query(
                Interaction
            )
            .filter(
                Interaction.user_id == user_id
            )
            .all()
        )

        if user_interactions:

            avg_watch_time = float(
                np.mean([
                    i.watch_time or 0
                    for i in user_interactions
                ])
            )

            avg_read_time = float(
                np.mean([
                    i.read_time or 0
                    for i in user_interactions
                ])
            )

            avg_scroll_depth = float(
                np.mean([
                    i.scroll_depth or 0
                    for i in user_interactions
                ])
            )

            click_rate = float(
                np.mean([
                    int(
                        i.clicked or False
                    )
                    for i in user_interactions
                ])
            )

            like_rate = float(
                np.mean([
                    int(
                        i.liked or False
                    )
                    for i in user_interactions
                ])
            )

            save_rate = float(
                np.mean([
                    int(
                        i.saved or False
                    )
                    for i in user_interactions
                ])
            )

            share_rate = float(
                np.mean([
                    int(
                        i.shared or False
                    )
                    for i in user_interactions
                ])
            )

        else:

            avg_watch_time = 0.0
            avg_read_time = 0.0
            avg_scroll_depth = 0.0

            click_rate = 0.0
            like_rate = 0.0
            save_rate = 0.0
            share_rate = 0.0

        # =========================================
        # 7. BUILD CANDIDATES
        # =========================================

        candidates = []

        for distance, idx in zip(
            distances[0],
            indices[0]
        ):

            # -----------------------------------------
            # Invalid FAISS result
            # -----------------------------------------

            if idx == -1:

                continue

            # -----------------------------------------
            # Protect against invalid mapping index
            # -----------------------------------------

            if idx >= len(self.id_mapping):

                continue

            # -----------------------------------------
            # Get content ID
            # -----------------------------------------

            content_id = (
                self.id_mapping[idx]
            )

            # -----------------------------------------
            # Skip consumed content
            # -----------------------------------------

            if content_id in consumed_ids:

                continue

            # -----------------------------------------
            # Get article
            # -----------------------------------------

            article = (
                self.db.query(
                    Content
                )
                .filter(
                    Content.id == content_id
                )
                .first()
            )

            if not article:

                continue

            # -----------------------------------------
            # Build article text
            # -----------------------------------------

            article_text = (
                f"{article.title or ''} "
                f"{article.description or ''} "
                f"{article.content_text or ''}"
            )

            # =========================================
            # 8. SEMANTIC SCORE
            # =========================================

            semantic_score = float(
                distance
            )

            # =========================================
            # 9. CATEGORY SCORE
            # =========================================

            category_score = float(
                category_preferences.get(
                    article.category,
                    0.0
                )
            )

            # =========================================
            # 10. PRODUCTIVITY SCORE
            # =========================================

            productivity_score = float(
                self.productivity_classifier
                .predict_productivity(
                    article_text
                )
            )

            # =========================================
            # 11. INTEREST CHANGE
            # =========================================

            interest_boost = float(
                self.get_interest_boost(
                    article.category,
                    interest_changes
                )
            )

            # =========================================
            # 12. LEARNED RANKING SCORE
            # =========================================
            #
            # IMPORTANT:
            # RankingModel uses predict_engagement()
            # NOT predict()
            # =========================================

            raw_ranking_score = float(
                self.ranking_model
                .predict_engagement(

                    clicked=click_rate,

                    liked=like_rate,

                    saved=save_rate,

                    shared=share_rate,

                    watch_time=avg_watch_time,

                    read_time=avg_read_time,

                    scroll_depth=avg_scroll_depth,

                    title_length=len(
                        article.title or ""
                    ),

                    description_length=len(
                        article.description or ""
                    )
                )
            )

            # =========================================
            # 13. STORE CANDIDATE
            # =========================================

            candidates.append({

                "content_id": content_id,

                "title": article.title,

                "category": article.category,

                "source": article.source,

                "url": article.url,

                "semantic_score": round(
                    semantic_score,
                    4
                ),

                "category_score": round(
                    category_score,
                    4
                ),

                "productivity_score": round(
                    productivity_score,
                    4
                ),

                "interest_boost": round(
                    interest_boost,
                    4
                ),

                "raw_ranking_score": (
                    raw_ranking_score
                ),

                "ranking_score": 0.0,

                "diversity_penalty": 0.0,

                "base_score": 0.0,

                "score": 0.0
            })

        # =========================================
        # 14. NORMALIZE RANKING MODEL OUTPUT
        # =========================================

        candidates = (
            self.normalize_ranking_scores(
                candidates
            )
        )

        # =========================================
        # 15. CALCULATE FINAL BASE SCORE
        # =========================================
        #
        # Semantic          = 30%
        # Category          = 15%
        # Productivity      = 20%
        # Learned Ranking   = 25%
        # Interest Trend    = 10%
        #
        # Total             = 100%
        # =========================================

        for candidate in candidates:

            candidate["base_score"] = (

                # -------------------------------------
                # Semantic similarity
                # -------------------------------------

                0.30
                * candidate["semantic_score"]

                # -------------------------------------
                # Category preference
                # -------------------------------------

                + 0.15
                * candidate["category_score"]

                # -------------------------------------
                # Productivity
                # -------------------------------------

                + 0.20
                * candidate["productivity_score"]

                # -------------------------------------
                # Learned engagement
                # -------------------------------------

                + 0.25
                * candidate["ranking_score"]

                # -------------------------------------
                # Interest trend
                # -------------------------------------

                + 0.10
                * candidate["interest_boost"]
            )

        # =========================================
        # 16. SORT BY BASE SCORE
        # =========================================

        candidates.sort(
            key=lambda x: x["base_score"],
            reverse=True
        )

        # =========================================
        # 17. DIVERSITY RE-RANKING
        # =========================================

        selected = []

        category_counts = {}

        max_same_category = 3

        for candidate in candidates:

            category = (
                candidate["category"]
            )

            count = (
                category_counts.get(
                    category,
                    0
                )
            )

            # -----------------------------------------
            # Diversity penalty
            # -----------------------------------------

            if count == 0:

                diversity_penalty = 0.0

            elif count == 1:

                diversity_penalty = 0.05

            elif count == 2:

                diversity_penalty = 0.10

            else:

                diversity_penalty = 0.20

            # -----------------------------------------
            # Final score
            # -----------------------------------------

            final_score = (
                candidate["base_score"]
                - diversity_penalty
            )

            candidate[
                "diversity_penalty"
            ] = round(
                diversity_penalty,
                4
            )

            candidate[
                "score"
            ] = round(
                final_score,
                4
            )

            # -----------------------------------------
            # Select candidate
            # -----------------------------------------

            if count < max_same_category:

                selected.append(
                    candidate
                )

                category_counts[
                    category
                ] = count + 1

            # -----------------------------------------
            # Stop when enough recommendations
            # -----------------------------------------

            if len(selected) >= top_k:

                break

        # =========================================
        # 18. FINAL SORT
        # =========================================

        selected.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        # =========================================
        # 19. REMOVE INTERNAL FIELDS
        # =========================================

        for item in selected:

            item.pop(
                "base_score",
                None
            )

            item.pop(
                "raw_ranking_score",
                None
            )

        # =========================================
        # 20. RETURN RECOMMENDATIONS
        # =========================================

        return selected[:top_k]
