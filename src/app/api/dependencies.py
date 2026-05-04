from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.api.auth import decode
from app.core import UserNotFoundError
from app.db import get_db
from app.repositories import UserRepository
from app.schemas import User
from app.services import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    user_repository = UserRepository(db)
    return UserService(user_repository)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service),
) -> User | None:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 1. Decode the Token
    token_data = decode(token)
    if token_data is None or "sub" not in token_data:
        raise credentials_exception

    # 2. Searches for the user by the UUID that is in the 'sub'
    try:
        user_uuid_id = UUID(token_data["sub"])
    except (ValueError, TypeError):
        raise credentials_exception

    try:
        user = user_service.get_by_uuid(user_uuid_id)
    except UserNotFoundError:
        raise credentials_exception

    if user and not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário inativo"
        )

    return user


async def admin_only(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores",
        )
    return current_user


async def authorize_user_access(
    user_id: int, current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_admin and current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: permissão insuficiente",
        )
    return current_user
