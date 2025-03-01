from fastapi import APIRouter
from app.services.estimation import EstimationService
from app.schemas.estimation import GetEstimationRequest, GetEstimationResponse


router = APIRouter(prefix="/optimal-route", tags=["estimation"])

estimationService = EstimationService()


@router.post("/", response_model=GetEstimationResponse)
def get_estimation(data: GetEstimationRequest):
    return estimationService.get_estimation(data)
