from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate
from app.database import SessionLocal
from ..utility import generate_custom_id
from sqlalchemy.sql import func
from sqlalchemy import Integer
from typing import Optional, Dict


class RestaurantService:
    def __init__(self):
        self.db = SessionLocal()
        self.initials = "R"

    def __del__(self):
        self.db.close()

    def get_all_restaurants(self):
        restaurants = self.db.query(Restaurant).all()
        return [
            {
                "id": restaurant.id,
                "name": restaurant.name,
            }
            for restaurant in restaurants
        ]

    def get_last_restaurant_id(self):
        last_restaurant = (
            self.db.query(Restaurant)
            .filter(Restaurant.id.like(self.initials + "%"))
            .order_by(func.cast(func.substr(Restaurant.id, 2), Integer).desc())
            .first()
        )
        return last_restaurant.id if last_restaurant else None

    def create_restaurant(self, restaurant: RestaurantCreate):
        last_restaurant_id = self.get_last_restaurant_id()
        new_restaurant_id = generate_custom_id(last_restaurant_id, self.initials)
        db_restaurant = Restaurant(
            id=new_restaurant_id,
            name=restaurant.name,
            latitude=restaurant.latitude,
            longitude=restaurant.longitude,
            avgPreparationTime=restaurant.avgPreparationTime,
        )
        self.db.add(db_restaurant)
        self.db.commit()
        self.db.refresh(db_restaurant)
        return db_restaurant

    def get_restaurants(self, skip: int = 0, limit: int = 10):
        return self.db.query(Restaurant).offset(skip).limit(limit).all()

    def get_restaurant_location(self, restaurant_id: str):
        restaurant = (
            self.db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        )
        if restaurant:
            return {
                "latitude": restaurant.latitude,
                "longitude": restaurant.longitude,
            }
        return None

    def get_restaurant_preparation_time(
        self, restaurant_id: str
    ) -> Optional[Dict[str, int]]:
        restaurant = (
            self.db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        )
        if restaurant:
            return {
                "avgPreparationTime": restaurant.avgPreparationTime,
            }
        return None
