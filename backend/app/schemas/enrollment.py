"""
Pydantic schemas for Enrollment model.
"""

from pydantic import BaseModel


class EnrollmentBase(BaseModel):
    user_id: int
    subject_id: int

    class Config:
        extra = "forbid"


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentUpdate(EnrollmentBase):
    pass


class EnrollmentPartialUpdate(BaseModel):
    user_id: int | None = None
    subject_id: int | None = None

    class Config:
        extra = "forbid"


class EnrollmentResponse(EnrollmentBase):
    id: int

    class Config:
        from_attributes = True
        extra = "forbid"
