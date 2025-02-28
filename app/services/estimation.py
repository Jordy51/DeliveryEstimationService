from app.services.restaurant import RestaurantService
from app.services.consumer import ConsumerService
from app.schemas.estimation import GetEstimationRequest, GetEstimationResponse
from ..utility import haversine, format_time, travel_time
from itertools import permutations
from app.schemas.estimation import OrderDetails


class EstimationService:
    def __init__(self):
        self.restaurantService = RestaurantService()
        self.consumerService = ConsumerService()

    @staticmethod
    def valid_order_sequences(orders: list[OrderDetails]):
        pairs = [(order.restaurantId, order.consumerId) for order in orders]
        unique_items = {item for pair in pairs for item in pair}
        valid_sequences = []

        for perm in permutations(unique_items):
            if all(perm.index(r) < perm.index(c) for r, c in pairs):
                valid_sequences.append(list(perm))

        return valid_sequences

    def _compute_total_time(
        self,
        order_routes,
        delivery_partner_location,
        restaurant_locations,
        consumer_locations,
        restaurant_prep_times,
    ):
        total_time = 0
        current_loc = {
            "latitude": delivery_partner_location.latitude,
            "longitude": delivery_partner_location.longitude,
        }
        for stop in order_routes:
            next_position = restaurant_locations.get(stop, consumer_locations.get(stop))
            if not next_position:
                continue

            distance = haversine(
                lat1=current_loc["latitude"],
                lon1=current_loc["longitude"],
                lat2=next_position["latitude"],
                lon2=next_position["longitude"],
            )
            total_time += travel_time(distance)
            current_loc = next_position

            preparation_time = (
                restaurant_prep_times.get(stop, {}).get("avgPreparationTime", 0) / 60
            )
            total_time = max(total_time, preparation_time)

        return total_time

    def _fetch_location_and_prep_times(self, orders: list[OrderDetails]):
        restaurant_locations, consumer_locations, restaurant_prep_times = {}, {}, {}
        for order in orders:
            restaurant_locations[order.restaurantId] = (
                self.restaurantService.get_restaurant_location(order.restaurantId)
            )
            restaurant_prep_times[order.restaurantId] = (
                self.restaurantService.get_restaurant_preparation_time(
                    order.restaurantId
                )
            )
            consumer_locations[order.consumerId] = (
                self.consumerService.get_consumer_location(order.consumerId)
            )
        return restaurant_locations, consumer_locations, restaurant_prep_times

    def _find_optimal_route(
        self,
        order_routes: list[list[str]],
        delivery_exec_location,
        restaurant_locations: dict,
        consumer_locations: dict,
        restaurant_prep_times: dict,
    ):
        route_time = [
            (
                route,
                self._compute_total_time(
                    order_routes=route,
                    delivery_partner_location=delivery_exec_location,
                    restaurant_locations=restaurant_locations,
                    consumer_locations=consumer_locations,
                    restaurant_prep_times=restaurant_prep_times,
                ),
            )
            for route in order_routes
        ]
        return min(route_time, key=lambda x: x[1])

    def get_estimation(self, data: GetEstimationRequest):
        restaurant_locations, consumer_locations, restaurant_prep_times = (
            self._fetch_location_and_prep_times(data.orders)
        )

        order_routes = self.valid_order_sequences(data.orders)
        optima_route, estimated_time = self._find_optimal_route(
            order_routes=order_routes,
            delivery_exec_location=data.deliveryExecLocation,
            restaurant_locations=restaurant_locations,
            consumer_locations=consumer_locations,
            restaurant_prep_times=restaurant_prep_times,
        )
        return GetEstimationResponse(
            optimalRoute=optima_route,
            estimatedTime=format_time(estimated_time),
        )
