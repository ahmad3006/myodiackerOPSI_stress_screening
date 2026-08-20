"""Decision fusion: gabungkan probabilitas biosinyal dan teks."""

from __future__ import annotations

from typing import Any, Optional

import numpy as np

from app.data.paths import STRESS_LABELS
from app.models.biosignal_model import biosignal_model
from app.models.text_model import text_model

BIO_WEIGHT_DEFAULT = 0.65
TEXT_WEIGHT_DEFAULT = 0.35


def _to_list(proba) -> list[float]:
    return [float(x) for x in np.asarray(proba, dtype=float)]


def _label_from_proba(proba: np.ndarray) -> int:
    return int(np.argmax(proba))


def extract_esp32_features(payload: dict[str, Any]) -> dict[str, Any]:
    """Ambil EMG/HRV/GSR dari JSON ESP32 tanpa mengubah logika prediksi.

    Alias yang didukung (siap ganti saat Serial/JSON aktual masuk):
    emg | emg_rms | EMG | EMG_RMS
    hrv | hrv_sdnn | HRV | HRV_SDNN
    gsr | gsr_tonic | GSR | GSR_TONIC
    text_post | text | caption
    """
    def pick(*keys: str, default=None):
        for key in keys:
            if key in payload and payload[key] is not None:
                return payload[key]
        return default

    return {
        "emg": float(pick("emg", "emg_rms", "EMG", "EMG_RMS", default=0.0)),
        "hrv": float(pick("hrv", "hrv_sdnn", "HRV", "HRV_SDNN", default=0.0)),
        "gsr": float(pick("gsr", "gsr_tonic", "GSR", "GSR_TONIC", default=0.0)),
        "text_post": pick("text_post", "text", "caption", default=None),
    }


def predict_stress(
    emg: float,
    hrv: float,
    gsr: float,
    text_post: Optional[str] = None,
    bio_weight: float = BIO_WEIGHT_DEFAULT,
    text_weight: float = TEXT_WEIGHT_DEFAULT,
) -> dict[str, Any]:
    """Inference utama. Input mentah (format ESP32), output status warna + level.

    Saat alat belum siap, panggil fungsi ini dengan dummy:
        predict_stress(emg=0.3, hrv=70.0, gsr=3.5, text_post="belajar dengan tenang")
    Nanti cukup ganti argumen dari JSON Serial, logika fusion tetap sama.
    """
    bio_proba = _to_list(biosignal_model.predict_proba(emg, hrv, gsr))
    text_proba = None

    has_text = bool(text_post and str(text_post).strip())
    if has_text:
        text_proba = _to_list(text_model.predict_proba(str(text_post).strip()))
        total = bio_weight + text_weight
        fused = (bio_weight / total) * np.array(bio_proba) + (text_weight / total) * np.array(
            text_proba
        )
        weights = {"biosignal": bio_weight / total, "text": text_weight / total}
    else:
        fused = np.array(bio_proba)
        weights = {"biosignal": 1.0, "text": 0.0}

    label = _label_from_proba(fused)
    meta = STRESS_LABELS[label]
    fused_list = _to_list(fused)

    return {
        "label": label,
        "level": meta["level"],
        "color": meta["color"],
        "status": meta["code"],
        "confidence": fused_list[label],
        "probabilities": {
            "normal": fused_list[0],
            "waspada": fused_list[1],
            "stres_tinggi": fused_list[2],
        },
        "details": {
            "biosignal_proba": bio_proba,
            "text_proba": text_proba,
            "weights": weights,
            "input": {
                "emg": float(emg),
                "hrv": float(hrv),
                "gsr": float(gsr),
                "text_post": text_post,
            },
        },
    }


def predict_from_esp32(
    payload: dict[str, Any],
    text_post: Optional[str] = None,
) -> dict[str, Any]:
    """Wrapper: parse payload JSON lalu panggil predict_stress."""
    features = extract_esp32_features(payload)
    if text_post is not None:
        features["text_post"] = text_post
    return predict_stress(
        emg=features["emg"],
        hrv=features["hrv"],
        gsr=features["gsr"],
        text_post=features["text_post"],
    )


class DecisionFusion:
    """Kompatibilitas API lama; delegasi ke predict_stress."""

    def fuse(self, biosignal: dict[str, Any], text_features: Any = None) -> dict[str, Any]:
        payload = dict(biosignal or {})
        if isinstance(text_features, dict):
            if "text_post" in text_features:
                payload["text_post"] = text_features["text_post"]
            elif "text" in text_features:
                payload["text_post"] = text_features["text"]
        elif isinstance(text_features, str):
            payload["text_post"] = text_features

        result = predict_from_esp32(payload)
        return {
            "decision": result["status"],
            "score": result["confidence"],
            "details": result,
        }
