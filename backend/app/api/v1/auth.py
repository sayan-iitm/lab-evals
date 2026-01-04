"""
Authentication endpoints for Google OAuth and JWT issuance.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.auth import (
    get_or_create_user_from_google,
    issue_jwt_for_user,
    verify_google_id_token,
)

router = APIRouter()


class TokenRequest(BaseModel):
    id_token: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=TokenResponse)
def login(request: TokenRequest):
    claims = verify_google_id_token(request.id_token)
    try:
        user = get_or_create_user_from_google(claims)
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )
    jwt = issue_jwt_for_user(user)
    return TokenResponse(access_token=jwt)
