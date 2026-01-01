"""
Pydantic schemas for Question model.
"""

from pydantic import BaseModel


class QuestionBase(BaseModel):
    subject_id: int
    text: str

    class Config:
        extra = "forbid"


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(QuestionBase):
    pass


class QuestionPartialUpdate(BaseModel):
    subject_id: int | None = None
    text: str | None = None

    class Config:
        extra = "forbid"


class QuestionResponse(QuestionBase):
    id: int

    class Config:
        from_attributes = True
        extra = "forbid"
