from pydantic import BaseModel


class RestaurantBase(BaseModel):
    name: str
    latitude: float
    longitude: float
    avgPreparationTime: int


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantResponse(RestaurantBase):
    id: str

    class Config:
        orm_mode = True
