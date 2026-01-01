"""
Admin endpoints for managing subjects, questions, and enrollments.
RBAC: Admin only.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import require_role
from app.constants.enums import UserRole
from app.core.database import SessionLocal
from app.models.question import Question
from app.models.subject import Subject
from app.models.user import User
from app.schemas.question import (
    QuestionCreate,
    QuestionResponse,
    QuestionUpdate,
)
from app.schemas.subject import SubjectCreate, SubjectResponse, SubjectUpdate
from app.schemas.user import UserCreate, UserResponse, UserUpdate

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
