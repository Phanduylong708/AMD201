from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.service import booking as booking_service
from src.service import rider as rider_service
#from src.service import user as user_service
from src.model import booking as booking_schemas
from src.model import rider as rider_schemas
from src.data.init import get_db



RIDER_SERVICE_URL = "http://localhost:8002/riders"
RIDE_MATCHING_URL = "http://localhost:8003/ride-matching"


router = APIRouter(prefix="/booking", tags=["booking"])


@router.post("/", response_model=booking_schemas.BookingResponse)
def create_booking(booking_data: booking_schemas.BookingCreate, db: Session = Depends(get_db)):
    """Create a new booking with automatic rider assignment."""
    return booking_service.create_booking_with_rider(db, booking_data)


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


@router.patch("/{booking_id}/status", response_model=booking_schemas.BookingResponse)
async def update_booking_status(
    booking_id: int,
    status_update: booking_schemas.BookingUpdateStatus,
    db: Session = Depends(get_db)
):
    """
    Update the status of a booking/ride.
    Status transitions:
    - Pending -> In Progress (when rider starts the ride)
    - In Progress -> Completed (when ride is finished)
    - Pending/In Progress -> Canceled (when either party cancels)
    """
    return booking_service.process_booking_status_update(db, booking_id, status_update.status)


@router.get("/status/{status}", response_model=list[booking_schemas.BookingResponse])
async def get_bookings_by_status(
    status: str,
    db: Session = Depends(get_db)
):
    """Get all bookings with a specific status."""
    if status not in ["Pending", "In Progress", "Completed", "Canceled"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    return booking_service.get_bookings_by_status(db, status)


@router.delete("/{booking_id}", status_code=204)
def delete_booking_endpoint(booking_id: int, db: Session = Depends(get_db)):
    """
    API endpoint to delete a booking by its ID.
    Returns 204 No Content on success.
    """
    booking_service.delete_booking(db, booking_id)