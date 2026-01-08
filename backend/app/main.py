"""
Entry point for the Lab Evaluation Application backend.
Initializes FastAPI app, includes API routers, and configures middleware.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import admin, auth, student, ta, user
from app.constants.enums import UserRole
from app.core.database import Base, SessionLocal, engine
from app.models.user import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure DB and all tables exist
    Base.metadata.create_all(bind=engine)

    # Auto-create admin user on startup
    db = SessionLocal()
    try:
        admin = (
            db.query(User).filter_by(email="sayan@study.iitm.ac.in").first()
        )
        if not admin:
            admin = User(
                name="Sayan",
                email="sayan@study.iitm.ac.in",
                role=UserRole.admin,
            )
            db.add(admin)
            db.commit()
        else:
            admin.role = UserRole.admin
            db.commit()
    finally:
        db.close()
    yield


app = FastAPI(title="Lab Evaluation Application", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API Routers
def include_routers(app: FastAPI):
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])
    app.include_router(ta.router, prefix="/api/v1/ta", tags=["ta"])
    app.include_router(
        student.router, prefix="/api/v1/student", tags=["student"]
    )
    app.include_router(user.router, prefix="/api/v1/user", tags=["user"])


include_routers(app)
