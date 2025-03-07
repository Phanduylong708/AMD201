from sqlalchemy.orm import Session
from src.data.models import Booking
from src.model import booking as schemas
from fastapi import Depends
from src.error import BookingError


def create_booking(db: Session, booking: schemas.BookingCreate):
    """Create a new booking in the database."""
    db_booking = Booking(
        user_id=booking.user_id,
        rider_id=booking.rider_id,
        status=booking.status,
        distance_km=booking.distance_km,
        fare=booking.fare
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def get_booking(db: Session, booking_id: int):
    """Retrieve a booking by ID."""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise BookingError.BOOKING_NOT_FOUND
    return booking


def update_booking_status(db: Session, booking_id: int, status: str):
    """Update the status of a booking."""
    booking = get_booking(db, booking_id)
    if not booking:
        raise BookingError.BOOKING_NOT_FOUND
    
    if status not in ["Pending", "In Progress", "Completed", "Canceled"]:
        raise BookingError.INVALID_BOOKING_STATUS
    
    booking.status = status
    db.commit()
    db.refresh(booking)
    return booking

