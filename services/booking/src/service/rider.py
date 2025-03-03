from sqlalchemy.orm import Session
from src.data.rider import Rider
from fastapi import HTTPException


def get_rider_by_id(db: Session, rider_id: int):
    """Retrieve a rider by ID."""
    rider = db.query(Rider).filter(Rider.id == rider_id).first()
    if not rider:
        raise HTTPException(status_code=404, detail="Rider not found")
    return rider


def get_available_riders(db: Session):
    """Retrieve all riders that are available (is_available=True, not in a ride)."""
    return db.query(Rider).filter(Rider.is_available == True, Rider.in_riding == False).all()

