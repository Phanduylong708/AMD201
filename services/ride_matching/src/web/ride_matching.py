from fastapi import APIRouter, HTTPException
from src.service.ride_matching import find_nearest_rider
from src.model.ride_matching import RideMatchRequest, RideMatchResponse

router = APIRouter(prefix="/ride-matching", tags=["Ride Matching"])

@router.post("/match-rider", response_model=RideMatchResponse)
def match_rider(request: RideMatchRequest):
    """Find the nearest available rider for a user."""
    try:
        rider, distance = find_nearest_rider(request.user_id)
        return {"rider_id": rider["id"], "distance_km": distance}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))