from fastapi import status

from app.core import AUTH_TOKEN_TYPE


def test_login_success(client, test_user):
    login_data = {
        "username": test_user.email,
        "password": "Mudar@123",  # Substitua pela senha real usada na fixture test_user
    }
    response = client.post("/auth/token", data=login_data)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == AUTH_TOKEN_TYPE


def test_login_invalid_password(client, test_user):
    login_data = {"username": test_user.email, "password": "wrong_password_123"}
    response = client.post("/auth/token", data=login_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Incorrect email or password"
