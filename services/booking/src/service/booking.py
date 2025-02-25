from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class BookingBase(BaseModel):
    user_id: int
    rider_id: int
    status: str = Field(..., regex="^(Pending|In Progress|Completed|Canceled)$")
    distance_km: float = Field(..., gt=0)
    fare: float = Field(..., gt=0)

class BookingCreate(BookingBase):
    pass

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

def calculate_fare(distance_km: float) -> int:
    """Tính giá cước dựa trên khoảng cách"""
    if distance_km <= 1:
        return int(distance_km * 10000)
    elif 2 <= distance_km <= 4:
        return int(distance_km * 15000)
    else:
        return int(distance_km * 12000)


