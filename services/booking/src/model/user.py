from pydantic import BaseModel, Field

class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    phone_number: str = Field(..., pattern=r'^\+?1?\d{9,15}$')

class UserCreate(UserBase):
    """Schema for creating a new user"""
    pass

class UserResponse(UserBase):
    """Schema for returning user data"""
    id: int

    class Config:
        from_attributes = True
