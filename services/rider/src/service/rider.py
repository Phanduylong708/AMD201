from sqlalchemy.orm import Session 
from fastapi import APIRouter
from src.model import rider as schemas
from src.data import rider as data_rider


router = APIRouter(prefix="/riders")


def create_rider(rider: schemas.RiderCreate, db: Session):  
    return data_rider.create_rider(rider, db)


def get_rider(db: Session, rider_id: int):
    return data_rider.get_rider(db, rider_id)


def get_riders(db: Session, skip: int = 0, limit: int = 100):
    return data_rider.get_riders(db, skip=skip, limit=limit)


def update_rider(db: Session, rider_id: int, rider: schemas.RiderUpdate, current_user: dict):
    return data_rider.update_rider(db, rider_id, rider, current_user)  


def delete_rider(db: Session, rider_id: int):
    return data_rider.delete_rider(db, rider_id)

def update_availability(db: Session, rider_id: int, is_available: bool):
    """Update rider availability status."""
    db_rider = get_rider(db, rider_id)
    if not db_rider:
        return None
    
    db_rider.is_available = is_available
    db.commit()
    db.refresh(db_rider)
    return {"is_available": db_rider.is_available}

def update_rider_status(db: Session, rider_id: int, is_available: bool, in_riding: bool):
    """Update both rider availability and riding status."""
    db_rider = get_rider(db, rider_id)
    if not db_rider:
        return None
    
    db_rider.is_available = is_available
    db_rider.in_riding = in_riding
    db.commit()
    db.refresh(db_rider)
    return db_rider

def get_available_riders(db: Session):
    """Retrieve all available riders who are not in a ride."""
    return db.query(data_rider).filter(data_rider.is_available == True, data_rider.in_riding == False).all()