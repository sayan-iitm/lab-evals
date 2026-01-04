from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, require_any_role
from app.constants.enums import UserRole
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter(
    dependencies=[
        Depends(
            require_any_role(
                [
                    UserRole.student,
                    UserRole.ta,
                    UserRole.admin,
                ]
            )
        )
    ]
)

# --- Get own user info ---


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
