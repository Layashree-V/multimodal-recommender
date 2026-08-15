from pathlib import Path

import joblib


class ProductivityClassifier:

    def __init__(self):

        model_path = Path(
            "trained_models/productivity_model.pkl"
        )

        self.model = None

        if model_path.exists():
            self.model = joblib.load(model_path)

    def predict_productivity(self, text: str) -> float:

        if not text:
            return 0.0

        # Model not trained yet
        if self.model is None:
            return 0.0

        probability = self.model.predict_proba(
            [text]
        )[0][1]

        return float(probability)