from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.service import rider as rider_service
from src.data.init import get_db
from src.data.models import get_rider_by_username, get_available_riders
from src.service.security import get_current_user, create_access_token, verify_password
from src.model import rider as schemas
from fastapi.responses import JSONResponse
from src.model.rider import LoginRequest


router = APIRouter(prefix="/riders")


#Use API Gateway for authentication
@router.post("/login")
def login_rider(login_data: LoginRequest, db: Session = Depends(get_db)):  
    """
    Rider login endpoint.
    """
    print(f"🔍 Attempting login for {login_data.username}")     #Debugging

    rider = get_rider_by_username(db, login_data.username)
    if not rider or not verify_password(login_data.password, rider.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": rider.username, "role": "rider"})

    return JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"},
        status_code=200
    )


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


# ✅ Update Rider Availability
@router.put("/{rider_id}/availability", response_model=schemas.RiderAvailabilityUpdate)
def update_availability(
    rider_id: int, 
    is_available: bool, 
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):  
    db_rider = rider_service.get_rider(db, rider_id)
    if not db_rider:
        raise HTTPException(status_code=404, detail="Rider not found")

    if current_user["sub"] != db_rider.username:
        raise HTTPException(status_code=403, detail="Not authorized to update availability.")

    return rider_service.update_availability(db, rider_id, is_available)


# ✅ Delete Rider Account (Only Self)
@router.delete("/{rider_id}", status_code=204)
def delete_rider(
    rider_id: int, 
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):  
    db_rider = rider_service.get_rider(db, rider_id)
    if not db_rider:
        raise HTTPException(status_code=404, detail="Rider not found")

    if current_user["sub"] != db_rider.username:
        raise HTTPException(status_code=403, detail="Not authorized to delete this rider.")

    success = rider_service.delete_rider(db, rider_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rider not found")
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
