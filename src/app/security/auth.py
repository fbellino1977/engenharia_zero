from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.settings import settings

# TODO: In the future, these constants will come from a .env file via Pydantic Settings
# Tip: use 'python -c "import secrets; print(secrets.token_urlsafe(32))"'
SECRET_KEY: str = settings.SECRET_KEY
ALGORITHM: str = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Context for password hashing using Argon2
pwd_context: CryptContext = CryptContext(schemes=["argon2"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks if the plain text password matches the stored hash
    """
    return bool(pwd_context.verify(plain_password, hashed_password))


def get_password_hash(password: str) -> str:
    """
    Generates a hash of a password using Argon2
    """
    return str(pwd_context.hash(password))


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    """
    Creates a signed JSON Web Token (JWT)

    Args:
        data: Dictionary containing the token claims (e.g., 'sub')
        expires_delta: Optional time for custom expiration
    """
    to_encode: dict[str, Any] = data.copy()

    if expires_delta:
        expire: datetime = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # O campo 'exp' é um padrão do JWT (Registered Claim Name)
    to_encode.update({"exp": expire})

    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any] | None:
    """
    Decodes a token and verifies its signature
    Returns None if the token is invalid or expired
    """
    try:
        payload: dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
