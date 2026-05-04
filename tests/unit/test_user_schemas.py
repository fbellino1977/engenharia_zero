import pytest
from pydantic import ValidationError

from app.schemas import UserCreate


def test_user_schema_success():
    """Valida que o schema aceita dados corretos"""
    payload = {
        "name": "Fabio",
        "email": "fabio@exemplo.com",
        "telephone": "11999999999",
        "birth_date": "1977-11-05T00:00:00",
        "password": "SenhaForte@123",
    }
    user = UserCreate(**payload)
    assert user.email == "fabio@exemplo.com"


def test_user_schema_invalid_email():
    """Valida que o Pydantic bloqueia e-mails malformados"""
    with pytest.raises(ValidationError):
        UserCreate(
            name="Erro",
            email="email-invalido",
            birth_date="1990-01-01T00:00:00",
            password="123",
        )


def test_user_schema_missing_fields():
    """Valida que o schema exige campos obrigatórios"""
    with pytest.raises(ValidationError):
        # Payload sem e-mail e sem senha
        UserCreate(name="Incompleto", birth_date="1990-01-01T00:00:00")


def test_user_schema_invalid_date_format():
    """Valida que o Pydantic rejeita formatos de data inválidos"""
    with pytest.raises(ValidationError):
        UserCreate(
            name="Data Errada",
            email="teste@teste.com",
            birth_date="05/11/1977",  # Formato incorreto (deve ser ISO 8601)
            password="123",
        )
