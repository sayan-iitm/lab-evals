"""
Entry point for the Lab Evaluation Application backend.
Initializes FastAPI app, includes API routers, and configures middleware.
"""

from fastapi import FastAPI

from app.api.v1 import admin, auth, student, ta

app = FastAPI(title="Lab Evaluation Application")


# API Routers
def include_routers(app: FastAPI):
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])
    app.include_router(ta.router, prefix="/api/v1/ta", tags=["ta"])
    app.include_router(
        student.router, prefix="/api/v1/student", tags=["student"]
    )


include_routers(app)
