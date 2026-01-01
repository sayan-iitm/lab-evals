"""
Enrollment model. Many-to-many User ↔ Subject. Role-aware.
"""

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Enrollment(Base):
    __tablename__ = "enrollments"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    subject_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("subjects.id"), nullable=False
    )
    user = relationship("User", backref="enrollments")
    subject = relationship("Subject", back_populates="enrollments")
