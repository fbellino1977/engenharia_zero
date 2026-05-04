from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import get_user_service
from app.core import AUTH_TOKEN_TYPE
from app.security import create_access_token
from app.services import UserService

router = APIRouter()


@router.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends(get_user_service),
) -> dict[str, str]:
    # 1. Authenticate user via service layer
    user = user_service.authenticate(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 2. Generate the JWT token
    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": AUTH_TOKEN_TYPE}
