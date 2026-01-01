"""
Pydantic schemas for Subject model.
"""

from pydantic import BaseModel


class SubjectBase(BaseModel):
    name: str
    description: str | None = None

    class Config:
        extra = "forbid"


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(SubjectBase):
    pass


class SubjectPartialUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

    class Config:
        extra = "forbid"


class SubjectResponse(SubjectBase):
    id: int

    class Config:
        from_attributes = True
        extra = "forbid"
