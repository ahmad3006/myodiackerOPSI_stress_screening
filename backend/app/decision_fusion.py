from typing import Dict, Any
from app.models import biosignal_model, text_model

class DecisionFusion:
    def __init__(self):
        self.biosignal_model = biosignal_model.load_model()
        self.text_model = text_model.load_model()

    def fuse(self, biosignal: Dict[str, float], text_features: Any) -> Dict[str, Any]:
        biosignal_score = self.biosignal_model.predict_proba([[
            biosignal.get("emg_rms", 0.0),
            biosignal.get("hrv_sdnn", 0.0),
            biosignal.get("gsr_tonic", 0.0)
        ]])[0][1]

        if hasattr(text_features, "text_vector"):
            vector = text_features.text_vector
        elif isinstance(text_features, dict) and "text_vector" in text_features:
            vector = text_features["text_vector"]
        else:
            vector = text_features if isinstance(text_features, dict) else {}

        text_vector = [float(v) for v in vector.values()] if isinstance(vector, dict) else []
        text_score = self.text_model.predict_proba([text_vector])[0][1]

        combined = (biosignal_score + text_score) / 2.0
        if combined > 0.75:
            decision = "HIGH_STRESS"
        elif combined > 0.45:
            decision = "WARNING"
        else:
            decision = "NORMAL"

        return {
            "decision": decision,
            "score": combined,
            "details": {
                "biosignal_score": biosignal_score,
                "text_score": text_score,
                "biosignal": biosignal,
                "text_vector": vector
            }
        }
