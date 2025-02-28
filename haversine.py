import math
from itertools import permutations

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in km
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi/2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c  # Distance in km

def travel_time(distance, speed=20):
    return distance / speed  # Time in hours

def compute_total_time(order_sequence,delivery_partner_location, locations, prep_times):
    total_time = 0
    current_loc = delivery_partner_location
    
    for stop in order_sequence:
        dist = haversine(current_loc[0], current_loc[1], locations[stop][0], locations[stop][1])
        total_time += travel_time(dist)
        
        if stop in prep_times:
            prep_time_hours = prep_times[stop] / 60  # Convert minutes to hours
            total_time = max(total_time, prep_time_hours)  # Wait if food is not ready yet
        
        current_loc = locations[stop]
    
    return total_time

def valid_order_sequences(base_sequence):
    valid_sequences = []
    
    for perm in permutations(base_sequence):
        if perm.index('R1') < perm.index('C1') and perm.index('R2') < perm.index('C2'):
            valid_sequences.append(list(perm))

    return valid_sequences


delivery_partner_location = (12.9352, 77.6245)
locations = {
    # 'Aman': (12.9352, 77.6245),  # Example starting point (Koramangala)
    'R1': (12.9400, 77.6200),  # Restaurant 1
    'R2': (12.9450, 77.6300),  # Restaurant 2
    'C1': (12.9500, 77.6350),  # Consumer 1
    'C2': (12.9550, 77.6400),  # Consumer 2
}

# Preparation times in hours
prep_times = {
    'R1': 55,  # 15 minutes
    'R2': 51,  # 20 minutes
}

def format_time(hours):
    minutes = int(round(hours * 60))
    return f"{minutes // 60}h {minutes % 60}m" if minutes >= 60 else f"{minutes}m"

def get_optimal_path(delivery_partner_location, locations, prep_times):
    valid_routes = valid_order_sequences(locations.keys())
    time_routes = [(route, compute_total_time(route, delivery_partner_location,locations, prep_times)) for route in valid_routes]
    return min(time_routes, key=lambda x: x[1])
    
optimal_route = get_optimal_path(delivery_partner_location, locations, prep_times)
print(f"Optimal Route: {' -> '.join(optimal_route[0])}")
print(f"Estimated Completion Time: {format_time(optimal_route[1])}")
