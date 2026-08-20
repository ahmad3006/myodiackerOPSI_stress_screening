"""Latih Random Forest (biosinyal) dan Naive Bayes (teks), lalu simpan pickle."""

from __future__ import annotations

import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

from app.data.dummy_data import generate_dummy_biosignal, generate_dummy_text
from app.data.paths import BIO_FEATURES, NB_MODEL_PATH, RF_MODEL_PATH, TFIDF_PATH


def train_biosignal_model(n_samples: int = 1000) -> dict:
    df = generate_dummy_biosignal(n_samples=n_samples)
    X = df[BIO_FEATURES]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        random_state=42,
        class_weight="balanced",
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = float(accuracy_score(y_test, y_pred))

    with open(RF_MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print(f"[Biosinyal] Akurasi uji 80:20 = {accuracy:.3f}")
    print(classification_report(y_test, y_pred, digits=3))
    print(f"[Biosinyal] Model disimpan: {RF_MODEL_PATH}")
    return {"accuracy": accuracy, "n_samples": n_samples, "path": str(RF_MODEL_PATH)}


def train_text_model() -> dict:
    texts, labels = generate_dummy_text()
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1, 2), max_features=500)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = MultinomialNB()
    model.fit(X_train_vec, y_train)
    y_pred = model.predict(X_test_vec)
    accuracy = float(accuracy_score(y_test, y_pred))

    with open(TFIDF_PATH, "wb") as f:
        pickle.dump(vectorizer, f)
    with open(NB_MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print(f"[NLP] Akurasi uji 80:20 = {accuracy:.3f}")
    print(classification_report(y_test, y_pred, digits=3))
    print(f"[NLP] Vectorizer disimpan: {TFIDF_PATH}")
    print(f"[NLP] Model disimpan: {NB_MODEL_PATH}")
    return {"accuracy": accuracy, "n_samples": len(texts), "path": str(NB_MODEL_PATH)}


def train_all(n_biosignal: int = 1000) -> dict:
    print("=== Pelatihan model MyoDiacker (data dummy) ===")
    bio = train_biosignal_model(n_samples=n_biosignal)
    nlp = train_text_model()
    return {"biosignal": bio, "nlp": nlp}


if __name__ == "__main__":
    train_all()
