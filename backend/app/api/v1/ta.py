"""
TA endpoints for creating and updating evaluations.
RBAC: TA only.
"""

from fastapi import APIRouter, Depends

from app.api.deps import require_role
from app.constants.enums import UserRole

router = APIRouter(dependencies=[Depends(require_role(UserRole.ta))])

# Placeholder for evaluation endpoints
