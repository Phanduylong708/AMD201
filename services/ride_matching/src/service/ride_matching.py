import requests
from sqlalchemy.orm import Session
from random import choice
from src.error import RideMatchingError

# Rider Service Base URL
RIDER_SERVICE_URL = "http://localhost:8002/riders"

# Simulated distance matrix
distance_matrix = {
    1: {1: 8, 2: 5, 3: 6, 4: 2, 5: 7},
    2: {1: 3, 2: 9, 3: 4, 4: 6, 5: 1},
    3: {1: 5, 2: 2, 3: 8, 4: 7, 5: 4},
    4: {1: 6, 2: 10, 3: 3, 4: 1, 5: 9},
    5: {1: 7, 2: 4, 3: 2, 4: 9, 5: 5},
}


def find_nearest_rider(user_id: int):
    """Find the nearest available rider using Rider Service API."""
    
    # Get available riders from Rider Service
    response = requests.get(f"{RIDER_SERVICE_URL}/available-riders")
    
    if response.status_code != 200:
        raise RideMatchingError.NO_RIDERS_AVAILABLE
    
    riders = response.json()  # Convert API response to Python list
    if not riders:
        raise RideMatchingError.USER_NOT_FOUND

    # if user_id not in distance_matrix:
    #     raise RideMatchingError("User not found in distance matrix")

    rider_distances = distance_matrix[user_id]
    nearest_distance = min(rider_distances.get(r["id"], float("inf")) for r in riders)
    closest_riders = [r for r in riders if rider_distances.get(r["id"]) == nearest_distance]

    selected_rider = choice(closest_riders)

    # Update rider status using Rider Service API
    requests.patch(f"{RIDER_SERVICE_URL}/{selected_rider['id']}/status", json={"is_available": False, "in_riding": True})

    return selected_rider, nearest_distance
