from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Engenharia Zero API ativa e conectada ao banco"}

def test_create_user():
    # We tested creating a new user
    response = client.post(
        "/users/",
        json={
            "id": 0,
            "name": "Test User", 
            "age": 25, 
            "email": "test@api.com"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test User"