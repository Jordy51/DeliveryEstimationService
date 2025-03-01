from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import Integer
from app.models.consumer import Consumer
from app.schemas.consumer import ConsumerCreate
from app.database import SessionLocal
from ..utility import generate_custom_id


class ConsumerService:
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()
        self.initials = "C"

    def __del__(self):
        self.close()

    def close(self):
        if self.db:
            self.db.close()

    def get_all_consumers(self):
        return [
            {"id": consumer.id, "name": consumer.name}
            for consumer in self.db.query(Consumer).all()
        ]

    def get_last_consumer_id(self):
        last_consumer = (
            self.db.query(Consumer)
            .filter(Consumer.id.like(f"{self.initials}%"))
            .order_by(func.cast(func.substr(Consumer.id, 2), Integer).desc())
            .first()
        )
        return last_consumer.id if last_consumer else None

    def create_consumer(self, consumer: ConsumerCreate):
        new_consumer_id = generate_custom_id(self.get_last_consumer_id(), self.initials)
        db_consumer = Consumer(
            id=new_consumer_id,
            name=consumer.name,
            latitude=consumer.latitude,
            longitude=consumer.longitude,
        )
        self.db.add(db_consumer)
        self.db.commit()
        self.db.refresh(db_consumer)
        return db_consumer

    def get_consumers(self, skip: int = 0, limit: int = 10):
        return self.db.query(Consumer).offset(skip).limit(limit).all()

    def get_consumer_location(self, consumer_id: str):
        consumer = self.db.query(Consumer).filter(Consumer.id == consumer_id).first()
        return (
            {"latitude": consumer.latitude, "longitude": consumer.longitude}
            if consumer
            else None
        )
