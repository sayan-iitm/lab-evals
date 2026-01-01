"""
Pydantic schemas for Evaluation model.
"""

from pydantic import BaseModel

from app.constants.enums import Marking


class EvaluationBase(BaseModel):
    student_id: int
    question_id: int
    ta_id: int
    marking: Marking
    remarks: str | None = None

    class Config:
        extra = "forbid"


class EvaluationCreate(EvaluationBase):
    pass


class EvaluationUpdate(EvaluationBase):
    pass


class EvaluationPartialUpdate(BaseModel):
    student_id: int | None = None
    question_id: int | None = None
    ta_id: int | None = None
    marking: Marking | None = None
    remarks: str | None = None

    class Config:
        extra = "forbid"


class EvaluationResponse(EvaluationBase):
    id: int

    class Config:
        from_attributes = True
        extra = "forbid"


class StudentEvaluationResponse(BaseModel):
    id: int
    student_id: int
    question_id: int
    ta_id: int
