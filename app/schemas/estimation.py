from pydantic import BaseModel


class LocationBase(BaseModel):
    latitude: float
    longitude: float


class OrderDetails(BaseModel):
    restaurantId: str
    consumerId: str


class GetEstimationRequest(BaseModel):
    deliveryExecLocation: LocationBase
    orders: list[OrderDetails]


class GetEstimationResponse(BaseModel):
    optimalRoute: list[str]
    estimatedTime: str

    class Config:
        orm_mode = True
