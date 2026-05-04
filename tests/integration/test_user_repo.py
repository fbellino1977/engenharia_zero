import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.db import UserTable
from app.repositories import UserRepository


def test_create_user_repository_success(db_session):
    """Valida que o repositório persiste o usuário corretamente no banco"""
    repo = UserRepository(db_session)
    from app.schemas import UserCreate

    user_in = UserCreate(
        name="Aline Repo",
        email="aline@repo.com",
        telephone="1144445555",
        birth_date="1986-05-13T00:00:00",
        password="hash_simulado",  # No repo, a senha já deve vir hasheada pela Service/API
    )

    created_user = repo.create(user_in)

    # Verifica se o ID foi gerado
    assert created_user.user_id is not None

    # Busca direta via SQLAlchemy para confirmar
    db_user = db_session.scalar(
        select(UserTable).where(UserTable.email == "aline@repo.com")
    )
    assert db_user.name == "Aline Repo"


def test_repo_get_hashed_password(db_session, test_user):
    """Verifica se o repositório recupera o hash de senha corretamente"""
    repo = UserRepository(db_session)
    hash_recuperado = repo.get_hashed_password(test_user.user_id)
    assert hash_recuperado == test_user.hashed_password


def test_db_unique_email_enforcement(db_session, test_user):
    """
    Garante que o banco de dados levanta erro de integridade em e-mails duplicados.
    Isso valida se o 'unique=True' no Model está funcionando.
    """
    duplicate_user = UserTable(
        name="Duplicado",
        email=test_user.email,  # E-mail já persistido pela fixture
        birth_date=test_user.birth_date,
        hashed_password="hash",
    )
    db_session.add(duplicate_user)

    with pytest.raises(IntegrityError):
        db_session.commit()
