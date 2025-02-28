from sqlalchemy import Column, String, Float,Integer
from app.database import Base

class Restaurant(Base):
    __tablename__ = "Restaurants"

    id = Column(String, primary_key=True, index=True, unique=True)
    name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    avgPreparationTime = Column(Integer)
