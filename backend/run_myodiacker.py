"""Entry point VS Code: latih model dummy lalu jalankan contoh inference.

Cara jalankan (folder backend):
    python run_myodiacker.py
    python run_myodiacker.py --retrain
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.data.paths import NB_MODEL_PATH, RF_MODEL_PATH, TFIDF_PATH
from app.data.train_models import train_all
from app.decision_fusion import predict_from_esp32, predict_stress


def models_ready() -> bool:
    return RF_MODEL_PATH.exists() and NB_MODEL_PATH.exists() and TFIDF_PATH.exists()


def run_demo() -> None:
    print("\n=== Demo inference (data dummy, bukan Serial Arduino) ===")
    samples = [
        {"emg": 0.20, "hrv": 82.0, "gsr": 2.8, "text_post": "belajar dengan tenang"},
        {"emg": 0.75, "hrv": 47.0, "gsr": 8.5, "text_post": "hari ini agak melelahkan"},
        {
            "emg": 1.50,
            "hrv": 24.0,
            "gsr": 16.0,
            "text_post": "hari ini sangat melelahkan dan saya tidak kuat",
        },
        {"emg": 1.40, "hrv": 27.0, "gsr": 15.2, "text_post": None},
    ]

    for i, sample in enumerate(samples, start=1):
        result = predict_stress(**sample)
        print(f"\nSampel {i}: {sample}")
        print(
            f"  -> {result['color']} | {result['level']} "
            f"(label={result['label']}, conf={result['confidence']:.3f})"
        )

    esp32_json = {
        "EMG_RMS": 0.71,
        "HRV_SDNN": 49.2,
        "GSR_TONIC": 8.1,
        "text_post": "saya mulai cemas karena tugas menumpuk",
    }
    fused = predict_from_esp32(esp32_json)
    print("\nContoh payload gaya ESP32 JSON:")
    print(json.dumps(esp32_json, ensure_ascii=False))
    print(
        f"  -> {fused['color']} | {fused['level']} "
        f"(label={fused['label']}, conf={fused['confidence']:.3f})"
    )
    print("\nNanti, ganti argumen predict_stress(...) dengan nilai dari Serial/JSON ESP32.")


def main() -> None:
    parser = argparse.ArgumentParser(description="MyoDiacker stress detector (dummy mode)")
    parser.add_argument("--retrain", action="store_true", help="Latih ulang model dummy")
    args = parser.parse_args()

    if args.retrain or not models_ready():
        train_all(n_biosignal=1000)
    else:
        print("Model pickle sudah ada, lewati pelatihan. Pakai --retrain untuk latih ulang.")

    run_demo()


if __name__ == "__main__":
    main()
