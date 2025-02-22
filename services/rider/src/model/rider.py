from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RiderBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    phone_number: str
    full_name: str
    vehicle_type: str
    license_plate: str
    rating: Optional[float] = Field(default=5.0, ge=0, le=5)
    is_available: bool = True

class RiderCreate(RiderBase):
    password: str = Field(..., min_length=8)

class RiderUpdate(BaseModel):
    phone_number: Optional[str] = None
    vehicle_type: Optional[str] = None
        
    rating: Optional[float] = Field(None, ge=0, le=5)
    is_available: Optional[bool] = None

class RiderInDB(RiderBase):
    id: int
    hashed_password: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class RiderResponse(RiderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True