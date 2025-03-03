from pydantic import BaseModel, EmailStr, Field, ConfigDict, validator
from typing import Optional
from datetime import datetime
import re
from src.error import UserError

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    phone_number: str = Field(..., pattern=r'^\+?1?\d{9,15}$')
    full_name: str = Field(..., min_length=1, max_length=100)

class UserCreate(UserBase):
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long and contain at least one letter and one number")
        if not re.search(r"[A-Za-z]", v) or not re.search(r"\d", v):
            raise ValueError("Password must be at least 8 characters long and contain at least one letter and one number")
        return v

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, pattern=r'^\+?1?\d{9,15}$')
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    
class UserInDB(UserBase):
    id: int
    hashed_password: str
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: str | None = None 