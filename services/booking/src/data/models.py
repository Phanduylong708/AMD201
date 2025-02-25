from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookingBase(BaseModel):
    user_id: int
    rider_id: int
    status: str
    distance_km: float
    fare: float

class BookingCreate(BookingBase):
    pass

class BookingUpdateStatus(BaseModel):
    status: str

class BookingResponse(BookingBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True