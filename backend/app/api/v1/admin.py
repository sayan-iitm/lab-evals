"""
Admin endpoints for managing subjects, questions, and enrollments.
RBAC: Admin only.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import require_role
from app.constants.enums import UserRole
from app.core.database import SessionLocal
from app.models.enrollment import Enrollment
from app.models.evaluation import Evaluation
from app.models.question import Question
from app.models.subject import Subject
from app.models.user import User
from app.schemas.enrollment import (
    EnrollmentCreate,
    EnrollmentResponse,
)
from app.schemas.evaluation import (
    EvaluationResponse,
    EvaluationUpdate,
)
from app.schemas.question import (
    QuestionCreate,
    QuestionResponse,
    QuestionUpdate,
)
from app.schemas.subject import SubjectCreate, SubjectResponse, SubjectUpdate
from app.schemas.user import UserCreate, UserResponse, UserUpdate

# --- User Endpoints ---

router = APIRouter(dependencies=[Depends(require_role(UserRole.admin))])

# --- Subject Endpoints ---


@router.post("/subjects", response_model=SubjectResponse)
def create_subject(subject: SubjectCreate):
    db = SessionLocal()
    try:
        db_obj = Subject(name=subject.name, description=subject.description)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    finally:
        db.close()


@router.get("/subjects/{subject_id}", response_model=SubjectResponse)
def get_subject(subject_id: int):
    db = SessionLocal()
    try:
        db_obj = db.query(Subject).filter_by(id=subject_id).first()
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subject not found",
            )
        return db_obj
    finally:
        db.close()


@router.get("/subjects", response_model=list[SubjectResponse])
def list_subjects():
    db = SessionLocal()
    try:
        return db.query(Subject).all()
    finally:
        db.close()


@router.put("/subjects/{subject_id}", response_model=SubjectResponse)
def update_subject(subject_id: int, subject: SubjectUpdate):
    db = SessionLocal()
    try:
        db_obj = db.query(Subject).filter_by(id=subject_id).first()
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subject not found",
            )
        db_obj.name = subject.name
        if subject.description is not None:
            db_obj.description = subject.description
        db.commit()
        db.refresh(db_obj)
        return db_obj
    finally:
        db.close()


@router.delete("/subjects/{subject_id}")
def delete_subject(subject_id: int):
    db = SessionLocal()
    try:
        db_obj = db.query(Subject).filter_by(id=subject_id).first()
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subject not found",
            )
        db.delete(db_obj)
        db.commit()
        return {}, status.HTTP_204_NO_CONTENT
    finally:
        db.close()


# --- Question Endpoints ---


@router.post("/questions", response_model=QuestionResponse)
def create_question(question: QuestionCreate):
    db = SessionLocal()
    try:
        subject = db.query(Subject).filter_by(id=question.subject_id).first()
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Subject does not exist",
            )
        db_obj = Question(subject_id=question.subject_id, text=question.text)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    finally:
        db.close()


@router.get("/questions/{question_id}", response_model=QuestionResponse)
def get_question(question_id: int):
    db = SessionLocal()
    try:
        db_obj = db.query(Question).filter_by(id=question_id).first()
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found",
            )
        return db_obj
    finally:
        db.close()


@router.get("/questions", response_model=list[QuestionResponse])
def list_questions():
    db = SessionLocal()
    try:
        return db.query(Question).all()
    finally:
        db.close()


@router.put("/questions/{question_id}", response_model=QuestionResponse)
def update_question(question_id: int, question: QuestionUpdate):
    db = SessionLocal()
    try:
        db_obj = db.query(Question).filter_by(id=question_id).first()
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found",
            )
        subject = db.query(Subject).filter_by(id=question.subject_id).first()
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Subject does not exist",
            )
        db_obj.subject_id = question.subject_id
        db_obj.text = question.text
        db.commit()
        db.refresh(db_obj)
        return db_obj
    finally:
        db.close()


@router.delete("/questions/{question_id}")
def delete_question(question_id: int):
    db = SessionLocal()
    try:
        db_obj = db.query(Question).filter_by(id=question_id).first()
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found",
            )
        db.delete(db_obj)
        db.commit()
        return {}, status.HTTP_204_NO_CONTENT
    finally:
        db.close()


# --- User Endpoints ---


@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    db = SessionLocal()
    try:
        db_obj = User(
            name=user.name,
            email=user.email,
            google_sub=user.google_sub,
            role=user.role,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    finally:
        db.close()


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    db = SessionLocal()
    try:
        db_obj = db.query(User).filter_by(id=user_id).first()
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return db_obj
    finally:
        db.close()


@router.get("/users", response_model=list[UserResponse])
def list_users():
    db = SessionLocal()
    try:
        return db.query(User).all()
    finally:
        db.close()


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate):
    db = SessionLocal()
    try:
        db_obj = db.query(User).filter_by(id=user_id).first()
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        db_obj.name = user.name
        db_obj.email = user.email
        if user.google_sub is not None:
            db_obj.google_sub = user.google_sub
        db_obj.role = user.role
        db.commit()
        db.refresh(db_obj)
        return db_obj
    finally:
        db.close()


@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    db = SessionLocal()
    try:
        db_obj = db.query(User).filter_by(id=user_id).first()
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        db.delete(db_obj)
        db.commit()
        return {}, status.HTTP_204_NO_CONTENT
    finally:
        db.close()


# --- Enrollment Endpoints ---


@router.post("/enrollments", response_model=EnrollmentResponse)
def create_enrollment(enrollment: EnrollmentCreate):
    db = SessionLocal()
    try:
        student = (
            db.query(User)
            .filter_by(id=enrollment.user_id, role=UserRole.student)
            .first()
        )
        if not student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not a student or does not exist",
            )
        subject = db.query(Subject).filter_by(id=enrollment.subject_id).first()
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Subject does not exist",
            )
        exists = (
            db.query(Enrollment)
            .filter_by(
                user_id=enrollment.user_id,
                subject_id=enrollment.subject_id,
            )
            .first()
        )
        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Enrollment already exists",
            )
        db_obj = Enrollment(
            user_id=enrollment.user_id, subject_id=enrollment.subject_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    finally:
        db.close()


@router.get("/enrollments/{enrollment_id}", response_model=EnrollmentResponse)
def get_enrollment(enrollment_id: int):
    db = SessionLocal()
    try:
        db_obj = db.query(Enrollment).filter_by(id=enrollment_id).first()
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found",
            )
        return db_obj
    finally:
        db.close()


@router.get("/enrollments", response_model=list[EnrollmentResponse])
def list_enrollments():
    db = SessionLocal()
    try:
        return db.query(Enrollment).all()
    finally:
        db.close()


@router.delete("/enrollments/{enrollment_id}")
def delete_enrollment(enrollment_id: int):
    db = SessionLocal()
    try:
        db_obj = db.query(Enrollment).filter_by(id=enrollment_id).first()
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found",
            )
        db.delete(db_obj)
        db.commit()
        return {}, status.HTTP_204_NO_CONTENT
    finally:
        db.close()


# == Evaluations


@router.get("/evaluations", response_model=list[EvaluationResponse])
def list_evaluations():
    db = SessionLocal()
    try:
        return db.query(Evaluation).all()
    finally:
        db.close()


@router.post("/evaluations/", response_model=EvaluationResponse)
def create_evaluation(
    evaluation: EvaluationUpdate,
):
    db = SessionLocal()
    try:
        student = (
            db.query(User)
            .filter_by(id=evaluation.student_id, role=UserRole.student)
            .first()
        )
        if not student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not a student or does not exist",
            )
        ta = (
            db.query(User)
            .filter_by(id=evaluation.ta_id, role=UserRole.ta)
            .first()
        )
        if not ta:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not a TA or does not exist",
            )
        question = (
            db.query(Question).filter_by(id=evaluation.question_id).first()
        )
        if not question:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Question does not exist",
            )
        enrollment = (
            db.query(Enrollment)
            .filter_by(
                user_id=evaluation.student_id, subject_id=question.subject_id
            )
            .first()
        )
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student is not enrolled in the subject",
            )
        exists = (
            db.query(Evaluation)
            .filter_by(
                student_id=evaluation.student_id,
                question_id=evaluation.question_id,
                ta_id=evaluation.ta_id,
            )
            .first()
        )
        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Evaluation already exists for this data",
            )
        db_obj = Evaluation(
            student_id=evaluation.student_id,
            question_id=evaluation.question_id,
            ta_id=evaluation.ta_id,
            marking=evaluation.marking,
            remarks=evaluation.remarks,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    finally:
        db.close()


@router.put("/evaluations/{evaluation_id}", response_model=EvaluationResponse)
def update_evaluation(
    evaluation_id: int,
    evaluation: EvaluationUpdate,
):
    db = SessionLocal()
    try:
        db_obj = db.query(Evaluation).filter_by(id=evaluation_id).first()
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evaluation not found",
            )
        student = (
            db.query(User)
            .filter_by(id=evaluation.student_id, role=UserRole.student)
            .first()
        )
        if not student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not a student or does not exist",
            )
        ta = (
            db.query(User)
            .filter_by(id=evaluation.ta_id, role=UserRole.ta)
            .first()
        )
        if not ta:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not a TA or does not exist",
            )
        question = (
            db.query(Question).filter_by(id=evaluation.question_id).first()
        )
        if not question:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Question does not exist",
            )
        enrollment = (
            db.query(Enrollment)
            .filter_by(
                student_id=evaluation.student_id,
                subject_id=question.subject_id,
            )
            .first()
        )
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student is not enrolled in the subject",
            )
        db_obj.student_id = evaluation.student_id
        db_obj.question_id = evaluation.question_id
        db_obj.ta_id = evaluation.ta_id
        db_obj.marking = evaluation.marking
        if evaluation.remarks is not None:
            db_obj.remarks = evaluation.remarks
        db.commit()
        db.refresh(db_obj)
        return db_obj
    finally:
        db.close()


@router.delete("/evaluations/{evaluation_id}")
def delete_evaluation(evaluation_id: int):
    db = SessionLocal()
    try:
        db_obj = db.query(Evaluation).filter_by(id=evaluation_id).first()
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evaluation not found",
            )
        db.delete(db_obj)
        db.commit()
        return {}, status.HTTP_204_NO_CONTENT
    finally:
        db.close()
