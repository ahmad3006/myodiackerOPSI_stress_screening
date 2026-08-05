from fastapi import APIRouter
from app.schemas import FusionRequest, FusionResponse
from app.decision_fusion import DecisionFusion

router = APIRouter(prefix="/api")

fusion_service = DecisionFusion()

@router.post("/fuse", response_model=FusionResponse)
def fuse(request: FusionRequest):
    result = fusion_service.fuse(
        biosignal=request.biosignal,
        text_features=request.text_features
    )
    return FusionResponse(
        decision=result["decision"],
        score=result["score"],
        details=result["details"]
    )
