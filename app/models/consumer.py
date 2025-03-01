from sqlalchemy import Column, String, Float
from app.database import Base


class Consumer(Base):
    __tablename__ = "Consumers"

    id = Column(String, primary_key=True, index=True, unique=True)
    name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
