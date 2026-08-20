from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class BiosignalFeatures(BaseModel):
    emg_rms: Optional[float] = None
    hrv_sdnn: Optional[float] = None
    gsr_tonic: Optional[float] = None
    emg: Optional[float] = None
    hrv: Optional[float] = None
    gsr: Optional[float] = None


class TextFeatures(BaseModel):
    text_post: Optional[str] = None
    text: Optional[str] = None
    text_vector: Optional[Dict[str, float]] = None


class FusionRequest(BaseModel):
    biosignal: BiosignalFeatures
    text_features: Optional[TextFeatures] = None


class FusionResponse(BaseModel):
    decision: str
    score: float
    details: Dict[str, Any]


class StressRequest(BaseModel):
    emg: float = Field(..., description="EMG dalam mV")
    hrv: float = Field(..., description="HRV dalam ms")
    gsr: float = Field(..., description="GSR dalam uS")
    text_post: Optional[str] = None


class StressResponse(BaseModel):
    label: int
    level: str
    color: str
    status: str
    confidence: float
    probabilities: Dict[str, float]
    details: Dict[str, Any]
