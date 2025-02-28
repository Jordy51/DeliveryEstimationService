from fastapi import APIRouter
from app.services.consumer import ConsumerService
from app.schemas.consumer import ConsumerCreate, ConsumerResponse


router = APIRouter(prefix="/consumer", tags=["consumer"])

consumerService = ConsumerService()


@router.get("/")
def get_items():
    return consumerService.get_all_consumers()


@router.post("/", response_model=ConsumerResponse)
def add_item(consumer: ConsumerCreate):
    return consumerService.create_consumer(consumer)
