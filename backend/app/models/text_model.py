import os
import pickle
import random

MODEL_PATH = "app/data/text_nb.pkl"

class DummyTextModel:
    def predict_proba(self, X):
        result = []
        for row in X:
            score = 0.5
            if len(row) > 0:
                score = sum(row) / max(1.0, len(row))
            score = min(max(score, 0.0), 1.0)
            result.append([1.0 - score, score])
        return result

class TextModel:
    def __init__(self):
        self.model = None

    def load_model(self):
        if self.model is None:
            if os.path.exists(MODEL_PATH):
                with open(MODEL_PATH, "rb") as f:
                    self.model = pickle.load(f)
            else:
                self.model = DummyTextModel()
        return self.model

text_model = TextModel()
