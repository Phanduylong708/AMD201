from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class BookingBase(BaseModel):
    user_id: int
    rider_id: int
    status: str = Field(..., pattern="^(Pending|In Progress|Completed|Canceled)$")
    distance_km: float = Field(..., gt=0)
    fare: float = Field(..., gt=0)

class BookingUpdate(BaseModel):
    status: str = Field(..., pattern="^(Pending|In Progress|Completed|Canceled)$")

class BookingInDB(BookingBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  #Updated for Pydantic v2

class BookingCreate(BaseModel):
    user_id: int
    rider_id: Optional[int] = None  #Initially no assigned rider
    distance_km: float
    fare: float = 0.0   #Changed to float for consistency
    status: str = "Pending"  #Default is Pending


class BookingUpdateStatus(BaseModel):  # ✅ FIXED: Changed from BookingUpdate
    status: str = Field(..., pattern="^(Pending|In Progress|Completed|Canceled)$")


class BookingResponse(BookingInDB):
    pass
