from sqlalchemy.orm import Session
from src.data.models import Booking
from src.model import booking as schemas
from src.error import BookingError


def create_booking(db: Session, booking_data: schemas.BookingCreate):
    """Create a new booking record in the database."""
    new_booking = Booking(**booking_data.dict())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


def get_booking_by_id(db: Session, booking_id: int):
    """Retrieve a booking record by its ID."""
    return db.query(Booking).filter(Booking.id == booking_id).first()


def update_booking_status_db(db: Session, booking_id: int, new_status: str):
    """Update the status of a booking record."""
    booking = get_booking_by_id(db, booking_id)
    if not booking:
        raise BookingError.booking_not_found("Booking not found")
    booking.status = new_status
    db.commit()
    db.refresh(booking)
    return booking


def list_bookings(db: Session):
    """Retrieve all bookings from the database."""
    return db.query(Booking).all()


def get_bookings_by_status(db: Session, status: str):
    """Retrieve all bookings with a specific status."""
    return db.query(Booking).filter(Booking.status == status).all()


def delete_booking(db: Session, booking_id: int):
    """Delete a booking by its ID."""
    booking = get_booking_by_id(db, booking_id)
    if not booking:
        raise BookingError.booking_not_found("Booking not found")
    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted successfully"}

