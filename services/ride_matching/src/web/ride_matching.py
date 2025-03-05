from fastapi import APIRouter, HTTPException
from src.service.ride_matching import find_all_available_riders
from src.model.ride_matching import RideMatchRequest, RideMatchResponse
from typing import List

router = APIRouter(prefix="/ride-matching", tags=["Ride Matching"])



@router.post("/match-rider-list", response_model=List[RideMatchResponse])
def match_rider_list(request: RideMatchRequest):
    """
    Returns a list of candidate riders sorted by distance for the given user.
    Each candidate is represented as an object with 'rider_id' and 'distance_km'.
    """
    try:
        candidate_list = find_all_available_riders(request.user_id)
        # Transform the list of tuples into a list of dicts
        result = [{"rider_id": rider["id"], "distance_km": distance} for rider, distance in candidate_list]
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))