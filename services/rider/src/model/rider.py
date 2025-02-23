from pydantic import BaseModel, Field
from typing import Optional, Literal

class RiderBase(BaseModel):
    username: str
    email: str
    full_name: str = Field(..., pattern=r'^[A-Za-z ]+$')  #Only allows letters and spaces
    vehicle_type: str
    license_plate: str
    password: str

#Create information 
class RiderCreate(RiderBase):
    username: str
    email: str
    phone_number: str = Field(..., pattern=r'^\d{10}$')  #10-digit validation
    full_name: str
    vehicle_type: Literal["motorbike", "car"]  #two option for vehicle type
    license_plate: str
    password: str  # Required for creation
    driving_licence: str = Field(..., pattern=r'^\d{12}$')  #Must be exactly 12 digits

class RiderResponse(BaseModel):
    id: int
    username: str
    email: str
    phone_number: str  #Stays as a string (prevents losing leading zeros)
    full_name: str = Field(..., pattern=r'^[A-Za-z ]+$')  #Only allows letters and spaces
    vehicle_type: str
    license_plate: str
    rating: Optional[float] = None
    is_available: bool
    in_riding: bool  # System-controlled

    class Config:
        orm_mode = True

#Update information 
class RiderUpdate(BaseModel):
    email: str
    password: str
    phone_number: str = Field(..., pattern=r'^\d{10}$')  #make sure valid
    vehicle_type: Optional[Literal["motorbike", "car"]] = None
    license_plate: Optional[str] = None


class RiderUpdateAvailability(BaseModel):
    is_available: Optional[bool] = None  #Riders update availability 