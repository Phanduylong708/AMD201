from sqlalchemy.orm import Session 
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from src.service import rider as rider_service
from src.model import rider as schemas
from src.service.security import get_current_user, create_access_token, verify_password
from src.data.models import get_rider_by_username
from src.data.init import get_db
from sqlalchemy.exc import IntegrityError
from src.data import rider as data_rider

router = APIRouter(prefix="/riders")

# ✅ Use API Gateway for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8000/gateway/login/rider")


def create_rider(rider: schemas.RiderCreate, db: Session):
    """
    Creates a new rider and ensures username, email, phone, and license plate are unique.
    """
    try:
        return data_rider.create_rider(rider, db)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username, Email, Phone, or License Plate already exists.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# ✅ Rider Login Endpoint
@router.post("/login")
def login_rider(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Rider login endpoint.
    """
    rider = get_rider_by_username(form_data.username)
    if not rider or not verify_password(form_data.password, rider.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": rider.username, "role": "rider"})
    
    return JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"},
        status_code=200
    )

# ✅ Get Current Rider Info
@router.get("/me", response_model=schemas.RiderResponse)
def read_riders_me(current_user: dict = Depends(get_current_user)):  
    return {"message": f"Rider info for {current_user['sub']}"}

# ✅ Update Rider Profile (Prevent Rating & Availability Changes)
@router.put("/{rider_id}", response_model=schemas.RiderResponse)
def update_rider(rider_id: int, rider: schemas.RiderUpdate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):  
    try:
        db_rider = rider_service.get_rider(rider_id)
        if not db_rider:
            raise HTTPException(status_code=404, detail="Rider not found")

        # 🔐 Ensure only the logged-in rider can update their own account
        if current_user["sub"] != db_rider.username:
            raise HTTPException(status_code=403, detail="Not authorized to update this rider.")

        update_data = rider.dict(exclude_unset=True)
        if "is_available" in update_data:
            del update_data["is_available"]  # Riders cannot manually update availability
        if "rating" in update_data:
            del update_data["rating"]  # Riders cannot manually update rating

        return rider_service.update_rider(rider_id, schemas.RiderUpdate(**update_data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# ✅ Delete Rider Account
@router.delete("/{rider_id}", status_code=204)
def delete_rider(rider_id: int, current_user: dict = Depends(get_current_user)):  
    try:
        db_rider = rider_service.get_rider(rider_id)
        if not db_rider:
            raise HTTPException(status_code=404, detail="Rider not found")

        # 🔐 Ensure only the logged-in rider can delete their own account
        if current_user["sub"] != db_rider.username:
            raise HTTPException(status_code=403, detail="Not authorized to delete this rider.")

        success = rider_service.delete_rider(rider_id)
        if not success:
            raise HTTPException(status_code=404, detail="Rider not found")
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# ✅ Update Rider Availability
@router.put("/{rider_id}/availability", response_model=schemas.RiderUpdateAvailability)
def update_availability(rider_id: int, is_available: bool, current_user: dict = Depends(get_current_user)):  
    db_rider = rider_service.get_rider(rider_id)
    if not db_rider:
        raise HTTPException(status_code=404, detail="Rider not found")

    # 🔐 Ensure only the logged-in rider can update their availability
    if current_user["sub"] != db_rider.username:
        raise HTTPException(status_code=403, detail="Not authorized to update availability.")

    return rider_service.update_rider(rider_id, schemas.RiderUpdate(is_available=is_available))
