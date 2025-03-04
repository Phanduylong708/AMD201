from pydantic import BaseModel, Field

class RideMatchRequest(BaseModel):
    """Request schema for finding a nearest rider"""
    user_id: int = Field(..., gt=0, description="ID of the user requesting a ride")

class RideMatchResponse(BaseModel):
    """Response schema when a rider is assigned"""
    rider_id: int
    distance_km: float

class RiderUpdateStatus(BaseModel):
    """Schema to update rider availability and ride status"""
    is_available: bool
    in_riding: bool
