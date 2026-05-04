from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import admin_only, get_current_user, get_user_service
from app.core import UserAlreadyExistsError, UserNotFoundError
from app.schemas import PasswordUpdate, User, UserCreate
from app.services import UserService

router = APIRouter()


@router.get("/user/me", response_model=User)
def read_user_me(current_user: User = Depends(get_current_user)) -> User | None:
    return current_user


@router.get("/", response_model=Sequence[User])
def read_users(
    skip: int = 0,
    limit: int = 10,
    user_service: UserService = Depends(get_user_service),
    _: User = Depends(admin_only),
) -> Sequence[User] | None:
    return user_service.get_all(skip, limit)


@router.get("/{user_id}", response_model=User)
def read_user_detail(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    _: User = Depends(admin_only),
) -> User | None:
    try:
        user = user_service.get_by_id(user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)

    return user


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    user_service: UserService = Depends(get_user_service),
    _: User = Depends(admin_only),
) -> User:
    # Business Rule Verification: Unique e-mail
    try:
        user_schema = user_service.create(user)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)

    return user_schema


@router.post("/me/password", status_code=status.HTTP_204_NO_CONTENT)
def update_password(
    password_data: PasswordUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> None:
    # 1. Checks if the current password matches the one in the database.
    try:
        current_password_exists = user_service.verify_current_password(
            current_user.user_id, password_data.current_password
        )
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    if not current_password_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Senha atual incorreta"
        )

    # 3. Persiste a mudança
    user_service.change_password(current_user.user_id, password_data.new_password)

    return None
