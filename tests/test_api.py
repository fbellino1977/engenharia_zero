def test_read_main(client):
    """Tests the root route to ensure the API is up and running"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Engenharia Zero API ativa e conectada ao banco"
    }


def test_create_user_api(client):
    """Tests user creation via HTTP POST"""
    user_data = {"name": "Test User", "age": 21, "email": "test@example.com"}
    response = client.post("/users/", json=user_data)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test User"
    assert "id" in data


def test_create_invoice_api_flow(client):
    """Tests the complete flow: User -> Product -> Invoice"""
    # 1. User Registration
    user_res = client.post(
        "/users/", json={"name": "Buyer", "age": 30, "email": "buyer@test.com"}
    )
    user_id = user_res.json()["id"]

    # 2. Product Registration
    prod_res = client.post("/products/", json={"name": "Keyboard", "price": 100.0})
    product_id = prod_res.json()["id"]

    # 3. Generates Invoice
    invoice_data = {
        "user_id": user_id,
        "items": [{"product_id": product_id, "quantity": 3}],
    }
    response = client.post("/invoices/", json=invoice_data)

    # 4. Validations
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["user_id"] == user_id
    assert len(res_data["items"]) == 1
    assert res_data["items"][0]["product_id"] == product_id
    assert res_data["total_price"] == 300.0


def test_create_invoice_rollback_api(client):
    """
    Tests whether the system cancels the creation of an Invoice if a product is invalid
    This validates whether 'db.rollback()' in 'main.py' is working
    """
    # 1. Creates the user (required for the user_id FK)
    user_res = client.post(
        "/users/", json={"name": "Ghost", "age": 40, "email": "ghost@test.com"}
    )
    user_id = user_res.json()["id"]

    # 2. Attempts to create invoice with non-existent product (ID 999)
    bad_invoice_data = {
        "user_id": user_id,
        "items": [
            {"product_id": 999, "quantity": 1}  # Not existent ID
        ],
    }

    response = client.post("/invoices/", json=bad_invoice_data)

    # 3. Verifications
    assert response.status_code == 400
    assert response.json()["detail"] == "Produto 999 não existe"

    # 4. The Final Test: The invoice must NOT exist in the database
    # We perform a GET request to list all invoices, and the result should be an empty list
    get_all_invoices = client.get("/invoices/")
    assert len(get_all_invoices.json()) == 0
