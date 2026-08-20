from fastapi import APIRouter

from app.decision_fusion import DecisionFusion, predict_stress
from app.schemas import FusionRequest, FusionResponse, StressRequest, StressResponse

router = APIRouter(prefix="/api")
fusion_service = DecisionFusion()


@router.post("/predict", response_model=StressResponse)
def predict(request: StressRequest):
    result = predict_stress(
        emg=request.emg,
        hrv=request.hrv,
        gsr=request.gsr,
        text_post=request.text_post,
    )
    return StressResponse(**result)


@router.post("/fuse", response_model=FusionResponse)
def fuse(request: FusionRequest):
    text_features = request.text_features.model_dump() if request.text_features else None
    result = fusion_service.fuse(
        biosignal=request.biosignal.model_dump(),
        text_features=text_features,
    )
    return FusionResponse(
        decision=result["decision"],
        score=result["score"],
        details=result["details"],
    )
