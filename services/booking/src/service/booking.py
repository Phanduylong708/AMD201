from sqlalchemy.orm import Session
from src.model import booking as schemas
from src.data import booking as models

def calculate_fare(distance_km: float) -> float:
    """Calculate fare based on a tiered pricing model."""
    if distance_km <= 1:
        return round(distance_km * 10000, 2)
    elif distance_km <= 4:
        return round(distance_km * 15000, 2)
    return round(distance_km * 12000, 2)

def create_booking(db: Session, booking_data: schemas.BookingCreate):
    """Create a new booking."""
    fare = calculate_fare(booking_data.distance_km)
    new_booking = models.Booking(**booking_data.dict(), fare=fare)
    
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

def get_booking_by_id(db: Session, booking_id: int):
    """Retrieve a booking by ID."""
    return db.query(models.Booking).filter(models.Booking.id == booking_id).first()

def update_booking_status(db: Session, booking_id: int, new_status: str):
    """Update the status of a booking."""
    booking = get_booking_by_id(db, booking_id)
    if not booking:
        return None
    booking.status = new_status
    db.commit()
    db.refresh(booking)
    return booking

def list_bookings(db: Session):
    """Retrieve all bookings."""
    return db.query(models.Booking).all()
