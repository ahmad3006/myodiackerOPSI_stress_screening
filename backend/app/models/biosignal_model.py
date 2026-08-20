"""Loader Random Forest untuk fitur EMG, HRV, GSR."""

from __future__ import annotations

import pickle

import pandas as pd

from app.data.paths import BIO_FEATURES, RF_MODEL_PATH


class BiosignalModel:
    def __init__(self) -> None:
        self.model = None

    def load_model(self):
        if self.model is None:
            if not RF_MODEL_PATH.exists():
                raise FileNotFoundError(
                    f"Model belum ada: {RF_MODEL_PATH}. Jalankan train_models.py dulu."
                )
            with open(RF_MODEL_PATH, "rb") as f:
                self.model = pickle.load(f)
        return self

    def predict_proba(self, emg: float, hrv: float, gsr: float):
        self.load_model()
        X = pd.DataFrame([[float(emg), float(hrv), float(gsr)]], columns=BIO_FEATURES)
        return self.model.predict_proba(X)[0]


biosignal_model = BiosignalModel()
