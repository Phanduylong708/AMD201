from fastapi import APIRouter, HTTPException, Depends
from typing import List
from src.service import rider as rider_service
from src.model import rider as schemas

router = APIRouter(prefix="/riders")

@router.post("/", response_model=schemas.RiderResponse, status_code=201)
def create_rider(rider: schemas.RiderCreate):
    return rider_service.create_rider(rider)

@router.get("/{rider_id}", response_model=schemas.RiderResponse)
def read_rider(rider_id: int):
    db_rider = rider_service.get_rider(rider_id)
    if not db_rider:
        raise HTTPException(status_code=404, detail="Rider not found")
    return db_rider

@router.get("/", response_model=List[schemas.RiderResponse])
def read_riders(skip: int = 0, limit: int = 100):
    return rider_service.get_riders(skip=skip, limit=limit)

@router.put("/{rider_id}", response_model=schemas.RiderResponse)
def update_rider(rider_id: int, rider: schemas.RiderUpdate):
    db_rider = rider_service.update_rider(rider_id, rider)
    if not db_rider:
        raise HTTPException(status_code=404, detail="Rider not found")
    return db_rider

@router.delete("/{rider_id}", status_code=204)
def delete_rider(rider_id: int):
    success = rider_service.delete_rider(rider_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rider not found")
    return None
