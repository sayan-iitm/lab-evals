"""
Pydantic schemas for User model.
"""

from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.constants.enums import UserRole


class UserBase(BaseModel):
    name: str
    email: EmailStr
    google_sub: str | None = None
    role: UserRole

    class Config:
        extra = "forbid"


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserPartialUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    google_sub: str | None = None
    role: UserRole | None = None

    class Config:
        extra = "forbid"


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        extra = "forbid"
