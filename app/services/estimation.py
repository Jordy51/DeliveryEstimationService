from app.services.restaurant import RestaurantService
from app.services.consumer import ConsumerService
from app.schemas.estimation import GetEstimationRequest, GetEstimationResponse
from ..utility import haversine, format_time, travel_time
from itertools import permutations
from app.schemas.estimation import OrderDetails
from fastapi import HTTPException


class EstimationService:
    def __init__(self):
        self.restaurantService = RestaurantService()
        self.consumerService = ConsumerService()

    @staticmethod
    def valid_order_sequences(orders: list[OrderDetails]):
        pairs = [(order.restaurantId, order.consumerId) for order in orders]
        unique_items = list({item for pair in pairs for item in pair})

        def is_valid_route(route):
            index_map = {place: i for i, place in enumerate(route)}
            return all(index_map[r] < index_map[c] for r, c in pairs)

        return [
            list(route) for route in permutations(unique_items) if is_valid_route(route)
        ]

    def _compute_total_time(
        self, route, delivery_exec_location, locations, prep_times, travel_cache
    ):
        total_time = 0
        current_loc = {
            "latitude": delivery_exec_location.latitude,
            "longitude": delivery_exec_location.longitude,
        }

        for stop in route:
            if stop not in locations:
                continue
            next_loc = locations[stop]

            loc_pair = (
                current_loc["latitude"],
                current_loc["longitude"],
                next_loc["latitude"],
                next_loc["longitude"],
            )
            if loc_pair not in travel_cache:
                travel_cache[loc_pair] = travel_time(
                    haversine(
                        current_loc["latitude"],
                        current_loc["longitude"],
                        next_loc["latitude"],
                        next_loc["longitude"],
                    )
                )
            total_time += travel_cache[loc_pair]

            total_time = max(total_time, prep_times.get(stop, 0))
            current_loc = next_loc

        return total_time

    def _fetch_location_and_prep_times(self, orders):
        restaurant_locations, consumer_locations, prep_times = {}, {}, {}
        for order in orders:
            rest_id, cons_id = order.restaurantId, order.consumerId
            if rest_id not in restaurant_locations:
                restaurant_data = self.restaurantService.get_restaurant_location(
                    rest_id
                )
                if restaurant_data is None:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Restaurant not found with id {rest_id} ",
                    )
                restaurant_locations[rest_id] = restaurant_data
                prep_times[rest_id] = (
                    self.restaurantService.get_restaurant_preparation_time(rest_id).get(
                        "avgPreparationTime", 0
                    )
                    / 60
                )
            if cons_id not in consumer_locations:
                consumer_data = self.consumerService.get_consumer_location(cons_id)
                if consumer_data is None:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Consumer not found with id {cons_id} ",
                    )
                consumer_locations[cons_id] = consumer_data

        return {**restaurant_locations, **consumer_locations}, prep_times

    def _find_optimal_route(
        self, order_routes, delivery_exec_location, locations, prep_times
    ):
        travel_cache = {}
        return min(
            (
                (
                    route,
                    self._compute_total_time(
                        route,
                        delivery_exec_location,
                        locations,
                        prep_times,
                        travel_cache,
                    ),
                )
                for route in order_routes
            ),
            key=lambda x: x[1],
        )

    def get_estimation(self, data: GetEstimationRequest):
        locations, prep_times = self._fetch_location_and_prep_times(data.orders)
        order_routes = self.valid_order_sequences(data.orders)
        optima_route, estimated_time = self._find_optimal_route(
            order_routes, data.deliveryExecLocation, locations, prep_times
        )

        return GetEstimationResponse(
            optimalRoute=optima_route,
            estimatedTime=format_time(estimated_time),
        )
