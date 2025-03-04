import requests
from random import choice
from fastapi import HTTPException

# Rider Service Base URL
RIDER_SERVICE_URL = "http://localhost:8002/riders"

# Simulated distance matrix - base matrix for 5x5 grid
base_distance_matrix = {
    1: {1: 8, 2: 5, 3: 6, 4: 2, 5: 7},
    2: {1: 3, 2: 9, 3: 4, 4: 6, 5: 1},
    3: {1: 5, 2: 2, 3: 8, 4: 7, 5: 4},
    4: {1: 6, 2: 10, 3: 3, 4: 1, 5: 9},
    5: {1: 7, 2: 4, 3: 2, 4: 9, 5: 5},
}

def map_id_to_matrix(id: int) -> int:
    """Maps any ID to a number between 1-5 for the distance matrix."""
    mapped_id = ((id - 1) % 5) + 1
    return mapped_id

def get_distance(user_id: int, rider_id: int) -> float:
    """Get distance between a user and rider using the base matrix."""
    mapped_user = map_id_to_matrix(user_id)
    mapped_rider = map_id_to_matrix(rider_id)
    return base_distance_matrix[mapped_user][mapped_rider]

def find_nearest_rider(user_id: int) -> tuple[dict, float]:
    """
    Find the nearest available rider using Rider Service API.
    Returns:
        tuple: (rider_dict, distance_km)
    Raises:
        HTTPException: If no riders available or service error
    """
    try:
        # Get available riders from Rider Service
        response = requests.get(f"{RIDER_SERVICE_URL}/available-riders")
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="No riders available from Rider Service")

        riders = response.json()
        if not riders:
            raise HTTPException(status_code=400, detail="No available riders found")

        # Calculate distances for all available riders
        rider_distance_list = []
        for rider in riders:
            rider_id = rider.get('id')
            if rider_id:
                distance = get_distance(user_id, rider_id)
                rider_distance_list.append((rider, distance))

        if not rider_distance_list:
            raise HTTPException(status_code=400, detail="Could not calculate distances for any riders")

        # Find the minimum distance
        nearest_distance = min(dist for _, dist in rider_distance_list)
        closest_riders = [r for r, dist in rider_distance_list if dist == nearest_distance]

        if not closest_riders:
            raise HTTPException(status_code=400, detail="No closest rider found")

        # Randomly select one of the closest riders
        selected_rider = choice(closest_riders)
        return selected_rider, nearest_distance

    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to communicate with Rider Service: {str(e)}"
        )
