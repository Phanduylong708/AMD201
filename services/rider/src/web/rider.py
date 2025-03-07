from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.service import rider as rider_service
from src.data.init import get_db
from src.data.models import get_rider_by_username, get_available_riders
from src.service.security import get_current_user, create_access_token, verify_password
from src.model import rider as schemas
from fastapi.security import OAuth2PasswordRequestForm
import requests


BOOKING_SERVICE_URL = "http://localhost:8004/booking"

router = APIRouter(prefix="/riders")


@router.post("/login")
def login_rider(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Extract username & password from form_data
    rider = get_rider_by_username(db, form_data.username)
    if not rider or not verify_password(form_data.password, rider.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": rider.username, "role": "rider"})
    return {"access_token": access_token, "token_type": "bearer"}


# ✅ Create a New Rider
@router.post("/", response_model=schemas.RiderResponse, status_code=201)
def create_rider(rider: schemas.RiderCreate, db: Session = Depends(get_db)):
    return rider_service.create_rider(rider, db)


# ✅ Get All Riders
@router.get("/", response_model=list[schemas.RiderResponse])
def get_riders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return rider_service.get_riders(db, skip=skip, limit=limit)


# ✅ Get Logged-in Rider's Information
@router.get("/me", response_model=schemas.RiderResponse)
def read_riders_me(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_rider = get_rider_by_username(db, current_user["sub"])
    if not db_rider:
        raise HTTPException(status_code=404, detail="Rider not found")
    return db_rider


# ✅ Update Rider Profile (Only Self, Cannot Change Rating or Availability)
@router.put("/{rider_id}", response_model=schemas.RiderResponse)
def update_rider(
    rider_id: int, 
    rider: schemas.RiderUpdate, 
    current_user: dict = Depends(get_current_user), 
    db: Session = Depends(get_db)
):  
    db_rider = rider_service.get_rider(db, rider_id)
    if not db_rider:
        raise HTTPException(status_code=404, detail="Rider not found")

    if current_user["sub"] != db_rider.username:
        raise HTTPException(status_code=403, detail="Not authorized to update this rider.")

    return rider_service.update_rider(rider_id, rider, current_user, db)


@router.get("/available-riders", response_model=list[schemas.RiderResponse])
def list_available_riders(db: Session = Depends(get_db)):
    """Returns all available riders."""
    return get_available_riders(db)


@router.put("/{rider_id}/availability", response_model=schemas.RiderAvailabilityUpdate)
def update_availability(
    is_available: bool, 
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):  
    # Retrieve the authenticated rider using the token
    db_rider = get_rider_by_username(db, current_user["sub"])
    if not db_rider:
        raise HTTPException(status_code=404, detail="Rider not found")

    # The current rider is allowed to update their own availability
    return rider_service.update_availability(db, db_rider.id, is_available)


@router.delete("/me", status_code=204)
def delete_my_account(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete the authenticated rider's account.
    Only the logged-in rider can delete their own account.
    """
    # Retrieve the rider from the database using the username in the token.
    db_rider = get_rider_by_username(db, current_user["sub"])
    if not db_rider:
        raise HTTPException(status_code=404, detail="Rider not found")

    # Delete the rider account.
    success = rider_service.delete_rider(db, db_rider.id)
    if not success:
        raise HTTPException(status_code=404, detail="Rider not found")
    
    # Return 204 No Content.
    return None

@router.patch("/{rider_id}/status")
def update_rider_status(
    rider_id: int,
    status_update: schemas.RiderStatusUpdate,
    db: Session = Depends(get_db)
):
    """
    Update rider's availability and riding status.
    This endpoint is used by the ride matching service.
    No authentication required for system-to-system communication.
    """
    try:
        db_rider = rider_service.get_rider(db, rider_id)
        if not db_rider:
            raise HTTPException(status_code=404, detail="Rider not found")
            
        # Update the rider's status
        return rider_service.update_rider_status(
            db, 
            rider_id, 
            status_update.is_available, 
            status_update.in_riding
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/accept-booking", response_model=dict)
def accept_booking(
    booking_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Endpoint for a rider to accept a booking.
    1. Retrieves the authenticated rider using the token.
    2. Updates the rider's status to busy (is_available=False, in_riding=True).
    3. Calls the Booking Service to update the booking status to 'In Progress'.
    """
    # Retrieve the rider from the database using the username in the token.
    db_rider = get_rider_by_username(db, current_user["sub"])
    if not db_rider:
        raise HTTPException(status_code=404, detail="Rider not found")
    
    # Update the rider's status to mark them as busy.
    updated_rider = rider_service.update_rider_status(db, db_rider.id, is_available=False, in_riding=True)
    if not updated_rider:
        raise HTTPException(status_code=400, detail="Failed to update rider status")

    # Call the Booking Service to update the booking status to 'In Progress'.
    response = requests.patch(
        f"{BOOKING_SERVICE_URL}/{booking_id}/status",
        json={"status": "In Progress"}
    )
    if response.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to update booking status: {response.text}"
        )

    return {"message": "Booking accepted. Rider is now in a ride and booking status updated to In Progress."}


@router.patch("/finish-riding", response_model=dict)
def finish_riding(
    booking_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Endpoint for a rider to finish a ride.
    1. Retrieves the authenticated rider using current_user.
    2. Updates the rider's status to available (is_available=True, in_riding=False).
    3. Calls the Booking Service to update the booking status to 'Completed'.
    """
    # Get the authenticated rider
    db_rider = get_rider_by_username(db, current_user["sub"])
    if not db_rider:
        raise HTTPException(status_code=404, detail="Rider not found")
    
    # Update rider status
    updated_rider = rider_service.update_rider_status(db, db_rider.id, is_available=True, in_riding=False)
    if not updated_rider:
        raise HTTPException(status_code=400, detail="Failed to update rider status")

    # Call Booking Service to update booking status to 'Completed'
    response = requests.patch(
        f"{BOOKING_SERVICE_URL}/{booking_id}/status",
        json={"status": "Completed"}
    )
    if response.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to update booking status: {response.text}"
        )
    
    return {"message": "Ride finished. Booking status set to Completed and rider is now available."}


@router.patch("/cancel-riding", response_model=dict)
def cancel_riding(
    booking_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Endpoint for a rider to cancel a ride.
    1. Retrieves the authenticated rider using current_user.
    2. Updates the rider's status to available (is_available=True, in_riding=False).
    3. Calls the Booking Service to update the booking status to 'Canceled'.
    """
    # Get the authenticated rider
    db_rider = get_rider_by_username(db, current_user["sub"])
    if not db_rider:
        raise HTTPException(status_code=404, detail="Rider not found")
    
    # Update rider status
    updated_rider = rider_service.update_rider_status(db, db_rider.id, is_available=True, in_riding=False)
    if not updated_rider:
        raise HTTPException(status_code=400, detail="Failed to update rider status")
    
    # Call Booking Service to update booking status to 'Canceled'
    response = requests.patch(
        f"{BOOKING_SERVICE_URL}/{booking_id}/status",
        json={"status": "Canceled"}
    )
    if response.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to update booking status: {response.text}"
        )
    
    return {"message": "Ride cancelled. Booking status set to Canceled and rider is now available."}