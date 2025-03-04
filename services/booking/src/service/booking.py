from sqlalchemy.orm import Session
from src.model import booking as schemas
from src.data import booking as models
from src.data.init import get_db
from fastapi import Depends
import requests
from fastapi import HTTPException

# Service URLs
RIDE_MATCHING_URL = "http://localhost:8003/ride-matching"
RIDER_SERVICE_URL = "http://localhost:8002/riders"

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
    # Update booking_data with the calculated fare
    booking_data.fare = fare
    new_booking = models.Booking(**booking_data.dict())
    
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


def get_booking_by_id(db: Session, booking_id: int):
    """Retrieve a booking by ID."""
    return db.query(models.Booking).filter(models.Booking.id == booking_id).first()


def update_booking_status_db(db: Session, booking_id: int, new_status: str):
    """
    Update the status of a booking.
    Returns:
        - Updated booking if successful
        - None if booking not found
    """
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


def get_bookings_by_status(db: Session, status: str):
    """Retrieve all bookings with a specific status."""
    return db.query(models.Booking).filter(models.Booking.status == status).all()


def validate_status_transition(current_status: str, new_status: str) -> bool:
    """
    Validate if the status transition is allowed.
    Rules:
    - Pending -> In Progress or Canceled
    - In Progress -> Completed or Canceled
    - Completed -> No further transitions
    - Canceled -> No further transitions
    """
    valid_transitions = {
        "Pending": ["In Progress", "Canceled"],
        "In Progress": ["Completed", "Canceled"],
        "Completed": [],  # Terminal state
        "Canceled": []   # Terminal state
    }
    
    return new_status in valid_transitions.get(current_status, [])


def update_booking_status(booking_id: int, update_data: schemas.BookingUpdateStatus, db: Session = Depends(get_db)):
    """API endpoint to update booking status."""
    updated_booking = update_booking_status_db(db, booking_id, update_data.status)
    return updated_booking


def find_nearest_rider(user_id: int) -> tuple[int, float]:
    """
    Find the nearest available rider using Ride Matching Service.
    Returns:
        tuple: (rider_id, distance_km)
    Raises:
        HTTPException: If no riders available or service error
    """
    try:
        match_response = requests.post(
            f"{RIDE_MATCHING_URL}/match-rider",
            json={"user_id": user_id}
        )
        
        if match_response.status_code != 200:
            raise HTTPException(status_code=400, detail="No available riders found")
            
        match_data = match_response.json()
        return match_data["rider_id"], match_data["distance_km"]
        
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to communicate with Ride Matching Service: {str(e)}"
        )


def create_booking_with_rider(db: Session, booking_data: schemas.BookingCreate):
    """
    Create a new booking with automatic rider assignment.
    Steps:
      1. Find the nearest available rider and retrieve the distance.
      2. Check if the selected rider already has an active booking 
         (with status "Pending" or "In Progress").
      3. If so, raise an HTTPException.
      4. Otherwise, set the booking details and create the booking record.
      5. Update the rider's status to not available and mark them as in a ride.
    """
    # 1. Find the nearest rider and get the distance
    rider_id, distance_km = find_nearest_rider(booking_data.user_id)
    
    # 2. Check if this rider already has an active booking
    existing_booking = db.query(models.Booking).filter(
        models.Booking.rider_id == rider_id,
        models.Booking.status.in_(["Pending", "In Progress"])
    ).first()
    if existing_booking:
        raise HTTPException(status_code=400, detail="Driver already has an active booking.")
    
    # 3. Set all required fields for the new booking
    booking_data.rider_id = rider_id
    booking_data.distance_km = distance_km
    booking_data.status = "Pending"
    booking_data.fare = calculate_fare(distance_km)
    
    # 4. Create the booking record in the database
    new_booking = create_booking(db, booking_data)
    
    # 5. Update the rider's status to mark them as busy (not available, in riding)
    update_rider_status(rider_id, is_available=False, in_riding=True)
    
    return new_booking


def update_rider_status(rider_id: int, is_available: bool, in_riding: bool) -> None:
    """
    Update rider status through Rider Service.
    Raises HTTPException if update fails.
    """
    try:
        response = requests.patch(
            f"{RIDER_SERVICE_URL}/{rider_id}/status",
            json={"is_available": is_available, "in_riding": in_riding}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to update rider status")
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to communicate with Rider Service: {str(e)}"
        )


def process_booking_status_update(db: Session, booking_id: int, new_status: str):
    """
    Process complete booking status update including rider status changes.
    Steps:
    1. Get and validate booking
    2. Validate status transition
    3. Update rider status if needed
    4. Update booking status
    """
    # Get current booking
    current_booking = get_booking_by_id(db, booking_id)
    if not current_booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Validate status transition
    if not validate_status_transition(current_booking.status, new_status):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition from {current_booking.status} to {new_status}"
        )

    # Update rider status based on booking status change
    # No need to update for "In Progress" since rider is already marked as in_riding=True
    if new_status in ["Completed", "Canceled"]:
        update_rider_status(current_booking.rider_id, is_available=True, in_riding=False)

    # Update booking status
    updated_booking = update_booking_status_db(db, booking_id, new_status)
    if not updated_booking:
        raise HTTPException(status_code=404, detail="Failed to update booking status")

    return updated_booking


def delete_booking(db: Session, booking_id: int):
    """Delete a booking by its ID."""
    booking = get_booking_by_id(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted successfully"}