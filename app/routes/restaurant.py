from fastapi import APIRouter
from app.services.restaurant import RestaurantService
from app.schemas.restaurant import RestaurantCreate, RestaurantResponse


router = APIRouter(prefix="/restaurant", tags=["restaurant"])

restaurantService = RestaurantService()


@router.get("/")
def get_items():
    return restaurantService.get_all_restaurants()


@router.post("/", response_model=RestaurantResponse)
def add_item(restaurant: RestaurantCreate):
    return restaurantService.create_restaurant(restaurant)
