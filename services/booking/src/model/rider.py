from pydantic import BaseModel, Field
from typing import Optional

class RiderBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    phone: str = Field(..., min_length=10, max_length=15, description="Rider's phone number")
    status: str = Field(default="Available", description="Rider availability status")
    vehicle_type: str = Field(..., min_length=1, max_length=50)
    license_plate: str = Field(..., min_length=3, max_length=15)
    rating: Optional[float] = Field(default=5.0, ge=0.0, le=5.0, description="Rider rating")

class RiderCreate(RiderBase):
    """Schema for creating a new rider"""
    pass

class RiderResponse(RiderBase):
    """Schema for returning rider data"""
    id: int

    class Config:
        from_attributes = True
