from pydantic import BaseModel, Field
from typing import Optional

class RiderBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=5, max_length=100)
    full_name: str = Field(..., min_length=1, max_length=100)
    phone_number: str = Field(..., min_length=10, max_length=10)
    is_available: bool = Field(default=True, description="Rider availability status")
    vehicle_type: str = Field(..., min_length=3, max_length=9, description="Vehicle type")
    license_plate: str = Field(..., min_length=3, max_length=20, description="License plate")
    driving_licence: str = Field(..., min_length=12, max_length=12, description="Driving license")
    rating: Optional[float] = Field(default=5.0, ge=0.0, le=5.0, description="Rider rating")
    in_riding: Optional[bool] = Field(default=False, description="Rider ride status")

class RiderResponse(RiderBase):
    """Schema for returning rider data"""
    id: int

    class Config:
        from_attributes = True  # ✅ Ensures SQLAlchemy model -> Pydantic conversion
