from datetime import timedelta
from typing import Any

from app.security import (
    create_access_token,
    decode_access_token,
)
from app.security import (
    get_password_hash as security_get_hash,
)


def create(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    return create_access_token(data)


def decode(data: str) -> dict[str, Any] | None:
    return decode_access_token(data)


def get_password_hash(password: str) -> str:
    return security_get_hash(password)
