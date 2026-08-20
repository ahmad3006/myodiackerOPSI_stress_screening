"""Loader TF-IDF + Multinomial Naive Bayes untuk teks Bahasa Indonesia."""

from __future__ import annotations

import pickle

from app.data.paths import NB_MODEL_PATH, TFIDF_PATH


class TextModel:
    def __init__(self) -> None:
        self.model = None
        self.vectorizer = None

    def load_model(self):
        if self.model is None or self.vectorizer is None:
            if not NB_MODEL_PATH.exists() or not TFIDF_PATH.exists():
                raise FileNotFoundError(
                    "Model NLP belum ada. Jalankan train_models.py untuk membuat "
                    f"{NB_MODEL_PATH.name} dan {TFIDF_PATH.name}."
                )
            with open(NB_MODEL_PATH, "rb") as f:
                self.model = pickle.load(f)
            with open(TFIDF_PATH, "rb") as f:
                self.vectorizer = pickle.load(f)
        return self

    def predict_proba(self, text_post: str):
        self.load_model()
        X = self.vectorizer.transform([text_post or ""])
        return self.model.predict_proba(X)[0]


text_model = TextModel()
