import pytest
from pydantic import ValidationError
from engenharia_zero.models import User


def test_user_creation_success():
    # Tests whether a valid User is created correctly
    user = User(id=1, name="Fabio", age="48", email="fabio@exemplo.com")
    assert user.name == "Fabio"
    assert user.id == 1


def test_user_creation_invalid_email():
    # Tests whether Pydantic raises the correct error for an invalid email address
    with pytest.raises(ValidationError):
        User(id=1, name="Erro", age="25", email="email-invalido")


def test_user_invalid_age():
    # Tests whether Pydantic raises the correct error for invalid age
    with pytest.raises(ValidationError):
        User(id=1, name="Erro", age=17, email="erro@exemple.com")
