from pydantic import BaseModel

class RideRequest(BaseModel):
    user_id: int
    latitude: float
    longitude: float

class RideResponse(BaseModel):
    user_id: int
    rider_id: int
    distance: float