from fastapi import status


def test_create_user_as_admin(client, admin_headers):
    """Garante que apenas admins podem criar novos usuários"""
    payload = {
        "name": "Novo User",
        "email": "novo@teste.com",
        "telephone": "1188888888",
        "birth_date": "2000-01-01T00:00:00",
        "password": "Senha@123",
    }
    response = client.post("/users/", json=payload, headers=admin_headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["email"] == "novo@teste.com"


def test_list_users_forbidden_for_common_user(client, user_headers):
    """Teste de Segurança: Usuário comum não pode listar a base total (403)"""
    response = client.get("/users/", headers=user_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_user_can_access_own_me_profile(client, user_headers, test_user):
    """Garante que o endpoint /user/me retorna os dados de quem está logado"""
    response = client.get("/users/user/me", headers=user_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == test_user.email


def test_update_password_flow(client, user_headers):
    """Valida o fluxo completo de alteração de senha via API"""
    payload = {"current_password": "Mudar@123", "new_password": "NovaSenhaForte@2026"}
    response = client.post("/users/me/password", json=payload, headers=user_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_create_user_duplicate_email_fails(client, admin_headers, test_user):
    """
    BR01: Should not allow the creation of a user with an already existing email address.
    Expected Status: 409 Conflict
    """
    payload = {
        "name": "Outro Fabio",
        "email": test_user.email,  # E-mail que já existe no banco via fixture
        "telephone": "11999999999",
        "birth_date": "1990-01-01T00:00:00",
        "password": "Senha@123",
    }
    response = client.post("/users/", json=payload, headers=admin_headers)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "E-mail já cadastrado no sistema"


def test_get_user_detail_not_found(client, admin_headers):
    """
    BR02: Should return 404 when searching for a non-existent ID
    Expected Status: 404 Not Found
    """
    non_existent_id = 9999
    response = client.get(f"/users/{non_existent_id}", headers=admin_headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert (
        response.json()["detail"] == f"Usuário com ID {non_existent_id} não encontrado"
    )


def test_update_password_wrong_current_password(client, user_headers):
    """
    BR03: Should fail if the current password entered is incorrect
    Expected Status: 400 Bad Request
    """
    payload = {
        "current_password": "SenhaErradaTotal",
        "new_password": "NovaSenhaForte@2026",
    }
    response = client.post("/users/me/password", json=payload, headers=user_headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Senha atual incorreta"
