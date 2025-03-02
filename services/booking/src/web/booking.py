from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.service import booking as booking_service
from src.model import booking as schemas
from src.data.init import get_db

router = APIRouter(prefix="/booking", tags=["booking"])

@router.post("/", response_model=schemas.BookingResponse)
def create_booking(booking_data: schemas.BookingCreate, db: Session = Depends(get_db)):
    """API endpoint to create a booking."""
    booking = booking_service.create_booking(db, booking_data)
    return booking

@router.get("/{booking_id}", response_model=schemas.BookingResponse)
def get_booking_by_id(booking_id: int, db: Session = Depends(get_db)):
    """API endpoint to retrieve a booking by ID."""
    booking = booking_service.get_booking_by_id(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.patch("/{booking_id}/status", response_model=schemas.BookingResponse)
def update_booking_status(booking_id: int, update_data: schemas.BookingUpdateStatus, db: Session = Depends(get_db)):
    """API endpoint to update booking status."""
    updated_booking = booking_service.update_booking_status(db, booking_id, update_data.status)
    if not updated_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return updated_booking

@router.get("/", response_model=list[schemas.BookingResponse])
def list_bookings(db: Session = Depends(get_db)):
    """API endpoint to list all bookings."""
    return booking_service.list_bookings(db)
