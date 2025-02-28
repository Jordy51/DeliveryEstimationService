from fastapi import APIRouter
from app.services.estimation import EstimationService
from app.schemas.estimation import GetEstimationRequest, GetEstimationResponse


router = APIRouter(prefix="/estimation", tags=["estimation"])


@router.get("/")
# TODO add get list of consumer and estimation
def get_items():
    return


@router.post("/", response_model=GetEstimationResponse)
def get_estimation(data: GetEstimationRequest):
    return EstimationService().get_estimation(data)
