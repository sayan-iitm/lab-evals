"""
Student endpoints for read-only access to own evaluations.
RBAC: Student only.
"""

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, require_role
from app.constants.enums import UserRole
from app.core.database import SessionLocal
from app.models.enrollment import Enrollment
from app.models.evaluation import Evaluation
from app.models.question import Question
from app.models.subject import Subject
from app.models.user import User
from app.schemas.enrollment import EnrollmentResponse
from app.schemas.evaluation import StudentEvaluationResponse
from app.schemas.question import QuestionResponse
from app.schemas.subject import SubjectResponse

router = APIRouter(dependencies=[Depends(require_role(UserRole.student))])

# --- Get own enrollments ---


@router.get("/enrollments", response_model=list[EnrollmentResponse])
def get_my_enrollments(current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    try:
        return (
            db.query(Enrollment)
            .filter(Enrollment.user_id == current_user.id)
            .all()
        )
    finally:
        db.close()


# --- Get subjects student is enrolled in ---


@router.get("/subjects", response_model=list[SubjectResponse])
def get_my_subjects(current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    try:
        subject_ids = (
            db.query(Enrollment.subject_id)
            .filter(Enrollment.user_id == current_user.id)
            .all()
        )
        subject_ids = [sid for (sid,) in subject_ids]
        return db.query(Subject).filter(Subject.id.in_(subject_ids)).all()
    finally:
        db.close()


# --- Get questions of enrolled subjects ---


@router.get("/questions", response_model=list[QuestionResponse])
def get_my_questions(current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    try:
        subject_ids = (
            db.query(Enrollment.subject_id)
            .filter(Enrollment.user_id == current_user.id)
            .all()
        )
        subject_ids = [sid for (sid,) in subject_ids]
        return (
            db.query(Question)
            .filter(Question.subject_id.in_(subject_ids))
            .all()
        )
    finally:
        db.close()


# --- Get own evaluations ---


@router.get("/evaluations", response_model=list[StudentEvaluationResponse])
def get_my_evaluations(current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    try:
        return (
            db.query(Evaluation)
            .filter(Evaluation.student_id == current_user.id)
            .all()
        )
    finally:
        db.close()
