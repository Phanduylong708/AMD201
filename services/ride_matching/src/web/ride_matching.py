from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.service.ride_matching import find_nearest_rider
from src.data.init import get_db
from src.model.ride_matching import RideMatchRequest, RideMatchResponse, RiderUpdateStatus
import requests


# Rider Service Base URL
RIDER_SERVICE_URL = "http://localhost:8002/riders"


router = APIRouter(prefix="/ride-matching", tags=["Ride Matching"])


@router.post("/match-rider", response_model=RideMatchResponse)
def match_rider(request: RideMatchRequest, db: Session = Depends(get_db)):
    """Find the nearest available rider for a user."""
    try:
        rider, distance = find_nearest_rider(request.user_id)
        return {"rider_id": rider["id"], "distance_km": distance}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.patch("/rider/{rider_id}/in-riding")
def in_riding(rider_id: int):
    """Marks a rider as currently in a ride (is_available=False, in_riding=True)."""
    
    # Debugging: Print the request being sent
    print(f"🔍 Sending PATCH request to Rider Service for Rider ID {rider_id}...")

    response = requests.patch(
        f"{RIDER_SERVICE_URL}/{rider_id}/status",
        json={"is_available": False, "in_riding": True}
    )

    print(f"🔍 Response Code: {response.status_code}")
    print(f"🔍 Response Body: {response.text}")  # 🔥 Debugging: Print the full response

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail=f"Failed to update rider to in_riding: {response.text}")

    return {"message": "Rider is now in a ride"}


@router.patch("/rider/{rider_id}/end-riding")
def end_riding(rider_id: int):
    """Marks a rider as finished with a ride (is_available=True, in_riding=False)."""
    response = requests.patch(
        f"{RIDER_SERVICE_URL}/{rider_id}/status",
        json={"is_available": True, "in_riding": False}
    )

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to update rider to end_riding")

    return {"message": "Rider has completed the ride and is now available"}