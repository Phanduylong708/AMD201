from fastapi import APIRouter, HTTPException
from typing import List
from src.service import rider as rider_service
from src.model import rider as schemas
from src.error import RiderError
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/riders")

@router.post("/", response_model=schemas.RiderResponse, status_code=201)
def create_rider(rider: schemas.RiderCreate):
    try:
        return rider_service.create_rider(rider)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username or Email already exists.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    


@router.get("/me", response_model=schemas.RiderResponse)
def read_riders_me():
    return {"message": "Rider info"}



@router.get("/{rider_id}", response_model=schemas.RiderResponse)
def read_rider(rider_id: int):
    try:
        db_rider = rider_service.get_rider(rider_id)
        if not db_rider:
            raise HTTPException(status_code=404, detail="Rider not found")
        return db_rider
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    


@router.get("/", response_model=List[schemas.RiderResponse])
def read_riders(skip: int = 0, limit: int = 100):
    return rider_service.get_riders(skip=skip, limit=limit)



@router.put("/{rider_id}", response_model=schemas.RiderResponse)
def update_rider(rider_id: int, rider: schemas.RiderUpdate):
    try:
        db_rider = rider_service.get_rider(rider_id)
        if not db_rider:
            raise HTTPException(status_code=404, detail="Rider not found")
        
        update_data = rider.dict(exclude_unset=True)
        if "is_available" in update_data:
            del update_data["is_available"]
        if "rating" in update_data:
            del update_data["rating"]
        
        return rider_service.update_rider(rider_id, schemas.RiderUpdate(**update_data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
   


@router.delete("/{rider_id}", status_code=204)
def delete_rider(rider_id: int):
    try:
        success = rider_service.delete_rider(rider_id)
        if not success:
            raise HTTPException(status_code=404, detail="Rider not found")
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    


#Update the availability of a rider logic
@router.put("/{rider_id}/availability", response_model=schemas.RiderUpdateAvailability)
def update_availability(rider_id: int, is_available: bool):
    db_rider = rider_service.get_rider(rider_id)
    if not db_rider:
        raise HTTPException(status_code=404, detail="Rider not found")
    return rider_service.update_rider(rider_id, schemas.RiderUpdate(is_available=is_available))


