"""
Student endpoints for read-only access to own evaluations.
RBAC: Student only.
"""

from fastapi import APIRouter, Depends

from app.api.deps import require_role
from app.constants.enums import UserRole

router = APIRouter(dependencies=[Depends(require_role(UserRole.student))])

# Placeholder for student endpoints
