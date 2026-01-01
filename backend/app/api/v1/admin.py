"""
Admin endpoints for managing subjects, questions, and enrollments.
RBAC: Admin only.
"""

from fastapi import APIRouter, Depends

from app.api.deps import require_role
from app.constants.enums import UserRole

router = APIRouter(dependencies=[Depends(require_role(UserRole.admin))])

# Placeholder for CRUD endpoints
