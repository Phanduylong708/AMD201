from pydantic import BaseModel, Field
from typing import Optional


class AvailabilityUpdate(BaseModel):
    is_available: bool


class RiderResponse(BaseModel):
    id: int
    username: str
    email: str
    phone_number: str  # Stays as a string (prevents losing leading zeros)
    full_name: str = Field(..., pattern=r'^[A-Za-z ]+$')  # Only allows letters and spaces
    vehicle_type: str
    license_plate: str
    rating: Optional[float] = None
    is_available: bool
    in_riding: bool  # System-controlled

    class Config:
        from_attributes = True