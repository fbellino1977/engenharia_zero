from fastapi import status


def test_read_root_health_check(client):
    """Garante que a rota principal de status está ativa"""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert "API ativa" in response.json()["message"]
