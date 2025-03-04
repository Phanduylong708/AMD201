from pydantic import BaseModel, Field
from typing import Optional, Literal

class LoginRequest(BaseModel):
    username: str
    password: str

class RiderBase(BaseModel):
    username: str
    email: str
    full_name: str = Field(..., pattern=r'^[A-Za-z ]+$')  # Only allows letters and spaces
    vehicle_type: str
    license_plate: str
    password: str

# Create information 
class RiderCreate(RiderBase):
    username: str
    email: str
    phone_number: str = Field(..., pattern=r'^\d{10}$')  # 10-digit validation
    full_name: str
    vehicle_type: Literal["motorbike", "car"]  # two options for vehicle type
    license_plate: str
    password: str 
    driving_licence: str = Field(..., pattern=r'^\d{12}$')  # Must be exactly 12 digits
    ride_count: Optional[int] = 0  # Correctly define ride_count as an optional integer with default 0

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

# Update information 
class RiderUpdate(BaseModel):
    email: str
    password: str
    phone_number: str = Field(..., pattern=r'^\d{10}$')  # Ensure valid
    vehicle_type: Optional[Literal["motorbike", "car"]] = None
    license_plate: Optional[str] = None

# Update availability
class RiderAvailabilityUpdate(BaseModel):
    is_available: bool

# Update riding status
class RiderIn_RidingUpdate(BaseModel):
    in_riding: bool

# Combined status update for system-to-system communication
class RiderStatusUpdate(BaseModel):
    is_available: bool
    in_riding: bool
