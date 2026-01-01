"""
Question model. Belongs to subject. Stores text and optional metadata.
"""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Question(Base):
    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    subject_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("subjects.id"), nullable=False
    )
    text: Mapped[str] = mapped_column(String(512), nullable=False)
    subject = relationship("Subject", back_populates="questions")
