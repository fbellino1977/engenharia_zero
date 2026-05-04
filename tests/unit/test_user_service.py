import pytest

from app.core import UserAlreadyExistsError
from app.repositories import UserRepository
from app.schemas import UserCreate
from app.services import UserService


@pytest.fixture
def user_service(db_session):
    """
    Fixture that sets up the Service with a real repository
    connected to the in-memory database
    """
    repository = UserRepository(db_session)
    return UserService(repository)


def test_create_user_service_success(user_service):
    # Setup
    user_in = UserCreate(
        name="Novo Usuário",
        email="novousuario@service.com",
        telephone="1133305456",
        birth_date="1996-07-11T00:00:00",
        password="password123",
    )

    # Act
    created_user = user_service.create(user_in)

    # Assert
    assert created_user.email == "novousuario@service.com"
    assert hasattr(
        created_user, "user_id"
    )  # Checks if you have obtained an ID from the database


def test_create_user_service_duplicate_email_raises_error(user_service):
    # Setup: We create the first user
    email = "duplicado@teste.com"
    user_in = UserCreate(
        name="Primeiro",
        email=email,
        telephone="1177743287",
        birth_date="2006-10-23T00:00:00",
        password="password123",
    )
    user_service.create(user_in)

    # Act & Assert: We tried create the second user with the same email
    user_duplicate = UserCreate(
        name="Segundo",
        email=email,
        telephone="1123238334",
        birth_date="2001-01-25T00:00:00",
        password="outrasenha",
    )

    with pytest.raises(UserAlreadyExistsError) as exc_info:
        user_service.create(user_duplicate)

    assert str(exc_info.value) == "E-mail já cadastrado no sistema"
