import os
import joblib
import numpy as np


class RankingModel:

    def __init__(self):

        # =====================================================
        # MODEL PATH
        # =====================================================

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
        )

        self.model_path = os.path.join(
            base_dir,
            "trained_models",
            "ranking_model.pkl"
        )

        self.model = None

        # =====================================================
        # LOAD MODEL
        # =====================================================

        if os.path.exists(self.model_path):

            self.model = joblib.load(
                self.model_path
            )

            print(
                "Ranking model loaded successfully."
            )

        else:

            print(
                "WARNING: Ranking model not found:"
            )

            print(
                self.model_path
            )

    # =========================================================
    # CHECK MODEL
    # =========================================================

    def is_available(self):

        return self.model is not None

    # =========================================================
    # PREDICT ENGAGEMENT
    # =========================================================

    def predict_engagement(
        self,
        clicked=0,
        liked=0,
        saved=0,
        shared=0,
        watch_time=0.0,
        read_time=0.0,
        scroll_depth=0.0,
        title_length=0,
        description_length=0
    ):

        if self.model is None:

            return 0.0

        features = np.array(
            [[
                clicked,
                liked,
                saved,
                shared,
                watch_time,
                read_time,
                scroll_depth,
                title_length,
                description_length
            ]],
            dtype=np.float32
        )

        prediction = self.model.predict(
            features
        )

        return float(
            prediction[0]
        )