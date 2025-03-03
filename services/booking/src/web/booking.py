from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.service import booking as booking_service
from src.service import rider as rider_service
#from src.service import user as user_service
from src.model import booking as booking_schemas
from src.model import rider as rider_schemas
from src.data.init import get_db


router = APIRouter(prefix="/booking", tags=["booking"])


@router.post("/", response_model=booking_schemas.BookingResponse)
def create_booking(booking_data: booking_schemas.BookingCreate, db: Session = Depends(get_db)):
    """API endpoint to create a booking."""
    booking = booking_service.create_booking(db, booking_data)
    return booking


@router.get("/id/{booking_id}", response_model=booking_schemas.BookingResponse)
def get_booking_by_id(booking_id: int, db: Session = Depends(get_db)):
    """API endpoint to retrieve a booking by ID."""
    booking = booking_service.get_booking_by_id(db, booking_id)
    return booking


@router.get("/", response_model=list[booking_schemas.BookingResponse])
def list_bookings(db: Session = Depends(get_db)):
    """API endpoint to list all bookings."""
    return booking_service.list_bookings(db)


@router.get("/available-riders", response_model=list[rider_schemas.RiderResponse])
def get_available_riders(db: Session = Depends(get_db)):
    """API endpoint to retrieve all available riders."""
    return rider_service.get_available_riders(db)