"""
JWT encoding and decoding helpers for authentication.
"""

from datetime import datetime, timedelta

from jose import JWTError, jwt

from app.core.config import get_settings

settings = get_settings()


def create_access_token(data: dict, expires_delta: int | None = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.now() + timedelta(
        minutes=expires_delta or settings.JWT_EXPIRES_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """Decode a JWT access token."""
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError as e:
        raise ValueError("Invalid token") from e
