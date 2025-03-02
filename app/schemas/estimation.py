from pydantic import BaseModel, field_validator


class LocationBase(BaseModel):
    latitude: float
    longitude: float


class OrderDetails(BaseModel):
    restaurantId: str
    consumerId: str


class GetEstimationRequest(BaseModel):
    deliveryExecLocation: LocationBase
    orders: list[OrderDetails]

    @field_validator("orders")
    @classmethod
    def check_orders_length(cls, orders):
        if 4 < len(orders):
            raise ValueError("The number of orders exceeds the allowed limit.")
        return orders


class GetEstimationResponse(BaseModel):
    optimalRoute: list[str]
    estimatedTime: str

    class Config:
        orm_mode = True
