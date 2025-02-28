import re
import math

def generate_custom_id(lastId:str|None, initials:str) -> str:
    print({"lastId":lastId})
    print({"initials":initials})
    if lastId and re.match(initials+r"\d+", lastId):
        initialsLen = len(initials)
        last_number = int(lastId[initialsLen:])
        return f"{initials}{last_number + 1}"
    return initials+"1"

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


def format_time(hours):
    minutes = int(round(hours * 60))
    return f"{minutes // 60}h {minutes % 60}m" if minutes >= 60 else f"{minutes}m"
