from sqlalchemy.orm import Session
from random import choice
from src.data.models import Rider
from src.data
from src.error import RideMatchingError

# Giả lập bảng khoảng cách
distance_matrix = {
    1: {1: 8, 2: 5, 3: 6, 4: 2, 5: 7},
    2: {1: 3, 2: 9, 3: 4, 4: 6, 5: 1},
    3: {1: 5, 2: 2, 3: 8, 4: 7, 5: 4},
    4: {1: 6, 2: 10, 3: 3, 4: 1, 5: 9},
    5: {1: 7, 2: 4, 3: 2, 4: 9, 5: 5},
}

def find_nearest_rider(user_id: int, db: Session):
    if user_id not in distance_matrix:
        raise RideMatchingError.USER_NOT_FOUND

    riders = db.query(Rider).filter(Rider.status == "Available").all()
    if not riders:
        raise RideMatchingError.NO_RIDERS_AVAILABLE

    rider_distances = distance_matrix[user_id]
    nearest_distance = min(rider_distances[r.id] for r in riders)
    closest_riders = [r for r in riders if rider_distances[r.id] == nearest_distance]

    selected_rider = choice(closest_riders)
    selected_rider.status = "Busy"
    db.commit()

    return selected_rider, nearest_distance
