from pydantic import BaseModel


class ConsumerBase(BaseModel):
    name: str
    latitude: float
    longitude: float


class ConsumerCreate(ConsumerBase):
    pass


class ConsumerResponse(ConsumerBase):
    id: str

    class Config:
        orm_mode = True
