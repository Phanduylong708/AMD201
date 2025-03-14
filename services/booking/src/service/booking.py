from sqlalchemy.orm import Session
from src.model import booking as schemas
from src.data import booking as models
from src.data.init import get_db
from fastapi import Depends
import requests
from fastapi import HTTPException
from src.error import BookingError
from src.data.booking import create_booking, get_booking_by_id, update_booking_status_db, list_bookings, get_bookings_by_status, delete_booking

# Service URLs
RIDE_MATCHING_URL = "http://localhost:8003/ride-matching"
RIDER_SERVICE_URL = "http://localhost:8002/riders"
USER_SERVICE_URL = "http://localhost:8001/users"

# User Service Functions
def check_user_exists(user_id: int) -> bool:
    """
    Check if a user exists through User Service API.
    Note: Since the User service requires authentication, we'll use a workaround
    by checking the list of all users instead of a direct user lookup.
    """
    try:
        # Get all users (this endpoint doesn't require authentication)
        response = requests.get(f"{USER_SERVICE_URL}/")
        if response.status_code != 200:
            return False
        
        # Check if the user ID exists in the list
        users = response.json()
        return any(user["id"] == user_id for user in users)
    except requests.RequestException:
        # If we can't reach the user service, assume user is not available
        return False


def calculate_fare(distance_km: float) -> float:
    """Calculate fare based on a tiered pricing model."""
    if distance_km <= 1:
        return round(distance_km * 10000, 2)
    elif distance_km <= 4:
        return round(distance_km * 15000, 2)
    return round(distance_km * 12000, 2)


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


def create_booking_with_rider(db: Session, booking_data: schemas.BookingCreate):

    # Step 1: Verify the user exists through User Service
    if not check_user_exists(booking_data.user_id):
        raise BookingError.booking_not_found("User not found or unavailable")
    
    # Step 2: Check if the user already has an active booking
    active_booking = db.query(models.Booking).filter(
        models.Booking.user_id == booking_data.user_id,
        models.Booking.status.in_(["Pending", "In Progress"])
    ).first()
    if active_booking:
        raise BookingError.active_booking_exists("User already has an active booking. Please wait for acceptance booking!")

    # Step 3: Check if the rider is already assigned to another booking
    if booking_data.rider_id:
        existing_booking = db.query(models.Booking).filter(
            models.Booking.rider_id == booking_data.rider_id,
            models.Booking.status.in_(["Pending", "In Progress"])
        ).first()
        if existing_booking:
            raise BookingError.rider_not_available("Selected rider is already assigned to another booking")

    # Step 4: Calculate fare and create booking
    if not booking_data.distance_km:
        raise BookingError.invalid_booking_data("Distance must be provided")
    
    booking_data.status = "Pending"
    booking_data.fare = calculate_fare(booking_data.distance_km)

    # Create the booking record
    new_booking = create_booking(db, booking_data)

    # Update the rider's status via Rider Service
    update_rider_status(booking_data.rider_id, is_available=False, in_riding=True)

    return new_booking

def update_rider_status(rider_id: int, is_available: bool, in_riding: bool) -> None:

    try:
        response = requests.patch(
            f"{RIDER_SERVICE_URL}/{rider_id}/status",
            json={"is_available": is_available, "in_riding": in_riding}
        )
        if response.status_code != 200:
            raise BookingError.rider_service_error("Failed to update rider status")
    except requests.RequestException as e:
        raise BookingError.rider_service_error(f"Failed to communicate with Rider Service: {str(e)}")


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
        raise BookingError.booking_not_found("Booking not found")

    # Validate status transition
    if not validate_status_transition(current_booking.status, new_status):
        raise BookingError.invalid_booking_status(f"Invalid status transition from {current_booking.status} to {new_status}")

    # Update rider status based on booking status change
    # No need to update for "In Progress" since rider is already marked as in_riding=True
    if new_status in ["Completed", "Canceled"]:
        update_rider_status(current_booking.rider_id, is_available=True, in_riding=False)

    # Update booking status
    updated_booking = update_booking_status_db(db, booking_id, new_status)
    if not updated_booking:
        raise BookingError.booking_not_found("Failed to update booking status")

    return updated_booking

