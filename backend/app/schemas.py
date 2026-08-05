from pydantic import BaseModel
from typing import Dict, Any

class BiosignalFeatures(BaseModel):
    emg_rms: float
    hrv_sdnn: float
    gsr_tonic: float

class TextFeatures(BaseModel):
    text_vector: Dict[str, float]

class FusionRequest(BaseModel):
    biosignal: BiosignalFeatures
    text_features: TextFeatures

class FusionResponse(BaseModel):
    decision: str
    score: float
    details: Dict[str, Any]
