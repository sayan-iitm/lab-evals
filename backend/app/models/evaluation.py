"""
Evaluation model.
Created by TA for a student and subject.
Contains marking, remarks, and per-question marks.
"""

from sqlalchemy import Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.constants.enums import Marking
from app.core.database import Base


class Evaluation(Base):
    __tablename__ = "evaluations"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    student_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("questions.id"), nullable=False
    )
    ta_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    marking: Mapped[Marking] = mapped_column(Enum(Marking), nullable=False)
    remarks: Mapped[str] = mapped_column(Text, nullable=True)

    student = relationship("User", foreign_keys=[student_id])
    ta = relationship("User", foreign_keys=[ta_id])
    question = relationship("Question")
