import os
import pickle

import numpy as np
import faiss

from app.models.interaction import Interaction


class UserProfileBuilder:

    def __init__(self, db):

        self.db = db

        # =================================================
        # LOAD FAISS INDEX
        # =================================================

        index_path = "trained_models/content.index"

        if not os.path.exists(index_path):

            raise FileNotFoundError(
                f"FAISS index not found: {index_path}"
            )

        self.index = faiss.read_index(
            index_path
        )

        # =================================================
        # LOAD ARTICLE ID MAPPING
        # =================================================

        mapping_path = (
            "trained_models/id_mapping.pkl"
        )

        if not os.path.exists(mapping_path):

            raise FileNotFoundError(
                f"ID mapping not found: {mapping_path}"
            )

        with open(
            mapping_path,
            "rb"
        ) as f:

            self.id_mapping = pickle.load(f)

        # =================================================
        # ARTICLE ID → FAISS POSITION
        # =================================================

        self.id_to_index = {
            content_id: index
            for index, content_id
            in enumerate(self.id_mapping)
        }

        print(
            f"UserProfileBuilder loaded "
            f"{len(self.id_mapping)} content vectors."
        )

    # =====================================================
    # BUILD USER PROFILE
    # =====================================================

    def build_profile(
        self,
        user_id: int
    ):

        # =================================================
        # GET USER INTERACTIONS
        # =================================================

        interactions = (
            self.db.query(Interaction)
            .filter(
                Interaction.user_id == user_id
            )
            .all()
        )

        embeddings = []
        weights = []

        # =================================================
        # BUILD PROFILE FROM INTERACTIONS
        # =================================================

        for interaction in interactions:

            content_id = (
                interaction.content_id
            )

            # ---------------------------------------------
            # Find article in FAISS
            # ---------------------------------------------

            faiss_position = (
                self.id_to_index.get(
                    content_id
                )
            )

            if faiss_position is None:
                continue

            # ---------------------------------------------
            # Get article embedding
            # ---------------------------------------------

            embedding = self.index.reconstruct(
                faiss_position
            )

            # ---------------------------------------------
            # Interaction weight
            # ---------------------------------------------

            weight = 1.0

            # Click
            if interaction.clicked:
                weight += 1.0

            # Like
            if interaction.liked:
                weight += 3.0

            # Save
            if interaction.saved:
                weight += 4.0

            # Share
            if interaction.shared:
                weight += 5.0

            # Watch time
            if interaction.watch_time:

                weight += min(
                    interaction.watch_time / 60.0,
                    3.0
                )

            # Read time
            if interaction.read_time:

                weight += min(
                    interaction.read_time / 60.0,
                    3.0
                )

            embeddings.append(
                embedding
            )

            weights.append(
                weight
            )

        # =================================================
        # NEW USER / NO VALID INTERACTIONS
        # =================================================

        if len(embeddings) == 0:

            if self.index.ntotal == 0:
                return None

            # ---------------------------------------------
            # Use average of all content vectors
            #
            # This gives a new user a neutral starting
            # recommendation profile.
            # ---------------------------------------------

            fallback = (
                self.index.reconstruct_n(
                    0,
                    self.index.ntotal
                )
            )

            fallback = np.asarray(
                fallback,
                dtype="float32"
            )

            user_vector = np.mean(
                fallback,
                axis=0
            )

            # Normalize
            norm = np.linalg.norm(
                user_vector
            )

            if norm > 0:

                user_vector = (
                    user_vector / norm
                )

            print(
                f"No valid interactions found "
                f"for user {user_id}. "
                f"Using neutral content profile."
            )

            return user_vector.tolist()

        # =================================================
        # NUMPY ARRAYS
        # =================================================

        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        weights = np.asarray(
            weights,
            dtype="float32"
        )

        # =================================================
        # WEIGHTED EMBEDDINGS
        # =================================================

        weighted_embeddings = (
            embeddings
            * weights[:, np.newaxis]
        )

        # =================================================
        # WEIGHTED AVERAGE
        # =================================================

        user_vector = (
            np.sum(
                weighted_embeddings,
                axis=0
            )
            / np.sum(weights)
        )

        # =================================================
        # NORMALIZE
        # =================================================

        norm = np.linalg.norm(
            user_vector
        )

        if norm > 0:

            user_vector = (
                user_vector / norm
            )

        # =================================================
        # DEBUG
        # =================================================

        print(
            "\n===================================="
        )

        print(
            "USER PROFILE CREATED"
        )

        print(
            "===================================="
        )

        print(
            "User ID:",
            user_id
        )

        print(
            "Interactions:",
            len(interactions)
        )

        print(
            "Valid embeddings:",
            len(embeddings)
        )

        print(
            "Total weight:",
            float(np.sum(weights))
        )

        print(
            "User vector dimension:",
            len(user_vector)
        )

        print(
            "User vector norm:",
            float(
                np.linalg.norm(
                    user_vector
                )
            )
        )

        print(
            "===================================="
        )

        return user_vector.tolist()