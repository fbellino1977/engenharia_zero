from fastapi import status


def test_read_main(client):
    """Tests the root route to ensure the API is up and running"""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": "Engenharia Zero API ativa e conectada ao banco"
    }


# --- Authorization Tests --- (ini)


def test_admin_can_list_users(client, admin_headers):
    """Ensures that the administrator user has access to the global list"""
    response = client.get("/users/", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_common_user_cannot_list_users(client, user_headers):
    """Ensures that Common User is blocked on the global list (403)"""
    response = client.get("/users/", headers=user_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Acesso restrito a administradores"


def test_user_can_access_own_profile(client, test_user, user_headers):
    """Luca accesses /users/{luca_id} -> Success"""
    response = client.get(f"/users/{test_user.user_id}", headers=user_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == test_user.email


def test_user_cannot_access_other_profile(client, test_admin, user_headers):
    """Luca tries to access /users/{admin_id} -> 403"""
    response = client.get(f"/users/{test_admin.user_id}", headers=user_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_password_success(client, user_headers):
    """It should allow the logged-in user to change their own password"""
    password_data = {
        "current_password": "Mudar@123",
        "new_password": "NovaSenhaForte@2026",
    }

    # Try updating your password
    response = client.patch(
        "/users/me/password", json=password_data, headers=user_headers
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Validation of "Force Login":
    # We tried to access a protected route with the OLD token.
    # If we implement token invalidation, this should return a 401.
    # For now, let's validate that logging in with the old password fails.
    login_data = {"username": "luca@exemplo.com", "password": "Mudar@123"}
    login_response = client.post("/auth/login", data=login_data)
    assert login_response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_password_wrong_current(client, user_headers):
    """You should not allow the change if the current password is incorrect"""
    password_data = {
        "current_password": "SenhaErrada@123",
        "new_password": "NovaSenhaForte@2026",
    }

    response = client.patch(
        "/users/me/password", json=password_data, headers=user_headers
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Senha atual incorreta"


# --- Authorization Tests --- (end)


def test_create_user_api(client, admin_headers):
    """Tests user creation via HTTP POST"""
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "telephone": "1144622173",
        "birth_date": "1999-11-05T00:00:00",
        "password": "password123",
    }
    response = client.post("/users/", json=user_data, headers=admin_headers)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Test User"
    assert "user_id" in data


def test_create_invoice_api_flow(client, admin_headers):
    """Tests the complete flow: User -> Product -> Invoice"""
    # 1. User Registration
    user_res = client.post(
        "/users/",
        json={
            "name": "Buyer",
            "email": "buyer@test.com",
            "telephone": "1166400954",
            "birth_date": "2000-01-11T00:00:00",
            "password": "password321",
        },
        headers=admin_headers,
    )
    user_data = user_res.json()
    user_id = user_res.json()["user_id"]
    user_uuid_id = str(user_data["user_uuid_id"])

    # 2. Product Registration
    prod_res = client.post(
        "/products/", json={"name": "Keyboard", "price": 100.0}, headers=admin_headers
    )
    product_id = prod_res.json()["product_id"]

    # 3. Generates Invoice
    invoice_data = {
        "user_uuid_id": user_uuid_id,
        "items": [{"product_id": product_id, "quantity": 3, "unit_price": 10.75}],
    }
    response = client.post("/invoices/", json=invoice_data, headers=admin_headers)

    # 4. Validations
    assert response.status_code == status.HTTP_200_OK
    res_data = response.json()
    assert res_data["user_id"] == user_id
    assert len(res_data["items"]) == 1
    assert res_data["items"][0]["product_id"] == product_id
    assert res_data["total_price"] == 300.0


def test_create_invoice_rollback_api(client, admin_headers):
    """
    Tests whether the system cancels the creation of an Invoice if a product is invalid
    This validates whether 'db.rollback()' in 'main.py' is working
    """
    # 1. Creates the user (required for the user_id FK)
    user_res = client.post(
        "/users/",
        json={
            "name": "Ghost",
            "email": "ghost@test.com",
            "telephone": "1174150100",
            "birth_date": "1980-05-13T00:00:00",
            "password": "pass#ABC@123",
        },
        headers=admin_headers,
    )
    user_data = user_res.json()
    user_uuid_id = str(user_data["user_uuid_id"])

    # 2. Attempts to create invoice with non-existent product (ID 999)
    bad_invoice_data = {
        "user_uuid_id": user_uuid_id,
        "items": [
            {
                "product_id": 999,  # Not existent Product ID
                "quantity": 1,
                "unit_price": 5.55,
            }
        ],
    }

    response = client.post("/invoices/", json=bad_invoice_data, headers=admin_headers)

    # 3. Verifications
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Produto 999 não existe"

    # 4. The Final Test: The invoice must NOT exist in the database
    # We perform a GET request to list all invoices, and the result should be an empty list
    get_all_invoices = client.get("/invoices/", headers=admin_headers)
    assert len(get_all_invoices.json()) == 0
