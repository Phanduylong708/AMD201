from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class BookingBase(BaseModel):
    user_id: int
    rider_id: int
    status: str = Field(..., regex="^(Pending|In Progress|Completed|Canceled)$")
    distance_km: float = Field(..., gt=0)
    fare: float = Field(..., gt=0)

class BookingUpdate(BaseModel):
    status: str = Field(..., regex="^(Pending|In Progress|Completed|Canceled)$")

class BookingInDB(BookingBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

class BookingResponse(BookingBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

class BookingCreate(BaseModel):
    user_id: int
    rider_id: Optional[int] = None  # Ban đầu chưa có tài xế
    distance_km: float
    fare: int = 0
    status: str = "Pending"  # Mặc định là Pending

class BookingResponse(BookingCreate):
    id: int
    status: str
