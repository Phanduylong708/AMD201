from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.service.ride_matching import find_nearest_rider
from src.model.ride_matching import RideRequest, RideResponse
from src.data.init import get_db

router = APIRouter()

@router.post("/match_rider", response_model=RideResponse)
def match_rider(request: RideRequest, db: Session = Depends(get_db)):
    try:
        rider, distance = find_nearest_rider(request.user_id, db)
        return RideResponse(user_id=request.user_id, rider_id=rider.id, distance=distance)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
