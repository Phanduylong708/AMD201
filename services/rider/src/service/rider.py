from src.data import rider as data_rider
from src.model import rider as schemas
from sqlalchemy.exc import IntegrityError

def create_rider(rider: schemas.RiderCreate):
    try:
        return data_rider.create_rider(rider)
    except IntegrityError:
        raise ValueError("Username or Email already exists.")  #Error response
    except Exception as e:
        raise ValueError(f"Unexpected error: {str(e)}")  #Catch unexpected issues

def get_rider(rider_id: int):
    return data_rider.get_rider(rider_id)

def get_riders(skip: int = 0, limit: int = 100):
    return data_rider.get_riders(skip=skip, limit=limit)

def update_rider(rider_id: int, rider: schemas.RiderUpdate):
    try:
        return data_rider.update_rider(rider_id, rider)
    except IntegrityError:
        raise ValueError("Username or Email already exists.")  #Error response
    except Exception as e:
        raise ValueError(f"Unexpected error: {str(e)}")  #Catch unexpected issues

def delete_rider(rider_id: int):
    return data_rider.delete_rider(rider_id)