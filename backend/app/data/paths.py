from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

RF_MODEL_PATH = DATA_DIR / "rf_biosensor.pkl"
TFIDF_PATH = DATA_DIR / "tfidf.pkl"
NB_MODEL_PATH = DATA_DIR / "nb_nlp.pkl"

STRESS_LABELS = {
    0: {"level": "Normal", "color": "Hijau", "code": "NORMAL"},
    1: {"level": "Waspada", "color": "Kuning", "code": "WARNING"},
    2: {"level": "Stres Tinggi", "color": "Merah", "code": "HIGH_STRESS"},
}

BIO_FEATURES = ["emg", "hrv", "gsr"]
