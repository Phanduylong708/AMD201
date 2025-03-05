import requests
from fastapi import HTTPException

# Rider Service Base URL (this service calls the Rider Service API)
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
    """Maps any ID to a number between 1 and 5 for the distance matrix."""
    return ((id - 1) % 5) + 1

def get_distance(user_id: int, rider_id: int) -> float:
    """Get distance between a user and a rider using the base matrix."""
    mapped_user = map_id_to_matrix(user_id)
    mapped_rider = map_id_to_matrix(rider_id)
    return base_distance_matrix[mapped_user][mapped_rider]

def find_all_available_riders(user_id: int) -> list[tuple[dict, float]]:
    """
    Retrieve all available riders from the Rider Service,
    compute their distance from the user using the simulated distance matrix,
    and return a sorted list (closest first) as tuples of (rider_dict, distance_km).
    """
    try:
        response = requests.get(f"{RIDER_SERVICE_URL}/available-riders")
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="No available riders from Rider Service")
        riders = response.json()
        if not riders:
            raise HTTPException(status_code=400, detail="No available riders found")

        rider_distance_list = []
        for rider in riders:
            rider_id = rider.get("id")
            if rider_id:
                distance = get_distance(user_id, rider_id)
                rider_distance_list.append((rider, distance))
        if not rider_distance_list:
            raise HTTPException(status_code=400, detail="Could not calculate distances for any riders")

        # Sort by distance (smallest first)
        rider_distance_list.sort(key=lambda x: x[1])
        return rider_distance_list

    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to communicate with Rider Service: {str(e)}"
        )

def find_nearest_rider(user_id: int) -> tuple[dict, float]:
    """
    Return the nearest available rider (the first element from the sorted list).
    """
    sorted_riders = find_all_available_riders(user_id)
    if not sorted_riders:
        raise HTTPException(status_code=400, detail="No available riders found")
    return sorted_riders[0]
