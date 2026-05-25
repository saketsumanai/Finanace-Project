"""
User Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema with common attributes."""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=8, max_length=100)


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Schema for user update."""
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None


class UserInDB(UserBase):
    """Schema for user in database."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserResponse(UserBase):
    """Schema for user response (without sensitive data)."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    role: str
    is_active: bool
    created_at: datetime


class Token(BaseModel):
    """Schema for authentication token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class TokenPayload(BaseModel):
    """Schema for JWT token payload."""
    sub: str  # user_id
    email: str
    role: str
    exp: datetime
    iat: datetime
