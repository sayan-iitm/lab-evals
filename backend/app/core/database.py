"""
Database engine and session configuration using SQLAlchemy 2.0 style.
Defines declarative base for models.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL, future=True, echo=(settings.ENV == "development")
)


class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(bind=engine, future=True)
