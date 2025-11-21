from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user model with common fields."""
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)


class UserCreate(UserBase):
    """User creation model with password."""
    password: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    """User login credentials."""
    email: EmailStr
    password: str


class User(UserBase):
    """User model returned to client (no password)."""
    id: str
    created_at: datetime
    is_active: bool = True
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "email": "user@example.com",
                "full_name": "John Doe",
                "created_at": "2024-01-01T00:00:00",
                "is_active": True
            }
        }


class UserInDB(UserBase):
    """User model as stored in database with hashed password."""
    id: str
    hashed_password: str
    created_at: datetime
    is_active: bool = True


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Data encoded in JWT token."""
    email: Optional[str] = None
