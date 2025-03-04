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
    # All other fields will be set automatically by the service
    rider_id: Optional[int] = None
    distance_km: Optional[float] = None
    fare: float = 0.0
    status: str = "Pending"

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1  # Only user_id is required
            }
        }

class BookingUpdateStatus(BaseModel):  # ✅ FIXED: Changed from BookingUpdate
    status: str = Field(..., pattern="^(Pending|In Progress|Completed|Canceled)$")

class BookingResponse(BookingInDB):
    pass
