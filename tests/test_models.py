import pytest
from pydantic import ValidationError
from engenharia_zero.models import User


def test_user_creation_success():
    # Testa se um usuário válido é criado corretamente
    user = User(id=1, name="Fabio", age="48", email="fabio@exemplo.com")
    assert user.name == "Fabio"
    assert user.id == 1


def test_user_creation_invalid_email():
    # Testa se o Pydantic levanta o erro correto para email inválido
    with pytest.raises(ValidationError):
        User(id=1, name="Erro", age="25", email="email-invalido")


def test_user_invalid_age():
    # Testa se o Pydantic levanta o erro correto para idade inválida
    with pytest.raises(ValidationError):
        User(id=1, name="Erro", age=17, email="erro@exemple.com")
