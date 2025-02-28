from app.models.consumer import Consumer
from app.schemas.consumer import ConsumerCreate
from app.database import SessionLocal
from ..utility import generate_custom_id
from sqlalchemy.sql import func
from sqlalchemy import Integer


class ConsumerService:
    def __init__(self):
        self.db = SessionLocal()
        self.initials = "C"

    def __del__(self):
        self.db.close()

    def get_all_consumers(self):
        consumers = self.db.query(Consumer).all()
        return [
            {
                "id": consumer.id,
                "name": consumer.name,
            }
            for consumer in consumers
        ]

    def get_last_consumer_id(self):
        last_consumer = (
            self.db.query(Consumer)
            .filter(Consumer.id.like(self.initials + "%"))
            .order_by(func.cast(func.substr(Consumer.id, 2), Integer).desc())
            .first()
        )
        return last_consumer.id if last_consumer else None

    def create_consumer(self, consumer: ConsumerCreate):
        last_consumer_id = self.get_last_consumer_id()
        new_consumer_id = generate_custom_id(last_consumer_id, self.initials)
        db_consumer = Consumer(
            id=new_consumer_id,
            name=consumer.name,
            latitude=consumer.latitude,
            longitude=consumer.longitude,
        )
        print(db_consumer)
        self.db.add(db_consumer)
        self.db.commit()
        self.db.refresh(db_consumer)
        return db_consumer

    def get_consumers(self, skip: int = 0, limit: int = 10):
        return self.db.query(Consumer).offset(skip).limit(limit).all()

    def get_consumer_location(self, consumer_id: str):
        consumer = self.db.query(Consumer).filter(Consumer.id == consumer_id).first()
        if consumer:
            return {"latitude": consumer.latitude, "longitude": consumer.longitude}
        return None
