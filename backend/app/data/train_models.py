import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle


def train_biosignal_model(data_path: str, output_path: str):
    df = pd.read_csv(data_path)
    X = df[["emg_rms", "hrv_sdnn", "gsr_tonic"]]
    y = df["stress_label"]
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    with open(output_path, "wb") as f:
        pickle.dump(model, f)


def train_text_model(texts: list[str], labels: list[int], output_model_path: str, output_vectorizer_path: str):
    vectorizer = TfidfVectorizer(max_features=500)
    X = vectorizer.fit_transform(texts)
    model = MultinomialNB()
    model.fit(X, labels)
    with open(output_model_path, "wb") as f:
        pickle.dump(model, f)
    with open(output_vectorizer_path, "wb") as f:
        pickle.dump(vectorizer, f)
