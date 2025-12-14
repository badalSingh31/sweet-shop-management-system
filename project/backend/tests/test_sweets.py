import pytest
from fastapi.testclient import TestClient


def get_auth_token(client: TestClient, user_data: dict) -> str:
    response = client.post("/api/auth/register", json=user_data)
    return response.json()["access_token"]


def test_get_sweets_unauthorized(client: TestClient):
    response = client.get("/api/sweets")
    assert response.status_code == 401


def test_get_sweets_authorized(client: TestClient, test_user_data):
    token = get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/sweets", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_sweet_as_user(client: TestClient, test_user_data, test_sweet_data):
    token = get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/sweets", json=test_sweet_data, headers=headers)
    assert response.status_code == 403


def test_search_sweets_by_name(client: TestClient, test_user_data):
    token = get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/sweets/search?name=chocolate", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_search_sweets_by_category(client: TestClient, test_user_data):
    token = get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/sweets/search?category=chocolate", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_search_sweets_by_price_range(client: TestClient, test_user_data):
    token = get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/sweets/search?min_price=1.0&max_price=5.0", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_purchase_sweet(client: TestClient, test_user_data):
    token = get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    sweets_response = client.get("/api/sweets", headers=headers)
    sweets = sweets_response.json()

    if sweets and len(sweets) > 0:
        sweet = sweets[0]
        original_quantity = sweet["quantity"]

        if original_quantity > 0:
            purchase_data = {"quantity": 1}
            response = client.post(
                f"/api/sweets/{sweet['id']}/purchase",
                json=purchase_data,
                headers=headers
            )
            assert response.status_code == 200
            purchase = response.json()
            assert purchase["quantity"] == 1
            assert float(purchase["total_price"]) == float(sweet["price"])


def test_purchase_insufficient_stock(client: TestClient, test_user_data):
    token = get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    sweets_response = client.get("/api/sweets", headers=headers)
    sweets = sweets_response.json()

    if sweets and len(sweets) > 0:
        sweet = sweets[0]
        purchase_data = {"quantity": 999999}
        response = client.post(
            f"/api/sweets/{sweet['id']}/purchase",
            json=purchase_data,
            headers=headers
        )
        assert response.status_code == 400
        assert "stock" in response.json()["detail"].lower()


def test_restock_as_user(client: TestClient, test_user_data):
    token = get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    sweets_response = client.get("/api/sweets", headers=headers)
    sweets = sweets_response.json()

    if sweets and len(sweets) > 0:
        sweet = sweets[0]
        restock_data = {"quantity": 10}
        response = client.post(
            f"/api/sweets/{sweet['id']}/restock",
            json=restock_data,
            headers=headers
        )
        assert response.status_code == 403
