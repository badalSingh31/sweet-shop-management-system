import pytest
from fastapi.testclient import TestClient


def test_register_user(client: TestClient, test_user_data):
    response = client.post("/api/auth/register", json=test_user_data)
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == test_user_data["email"]
    assert data["user"]["role"] == "user"


def test_register_duplicate_user(client: TestClient, test_user_data):
    client.post("/api/auth/register", json=test_user_data)
    response = client.post("/api/auth/register", json=test_user_data)
    assert response.status_code == 400
    assert "already" in response.json()["detail"].lower()


def test_register_invalid_email(client: TestClient):
    invalid_data = {
        "email": "invalid-email",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    response = client.post("/api/auth/register", json=invalid_data)
    assert response.status_code == 422


def test_register_short_password(client: TestClient):
    invalid_data = {
        "email": "test@example.com",
        "password": "123",
        "full_name": "Test User"
    }
    response = client.post("/api/auth/register", json=invalid_data)
    assert response.status_code == 422


def test_login_user(client: TestClient, test_user_data):
    client.post("/api/auth/register", json=test_user_data)

    login_data = {
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == test_user_data["email"]


def test_login_invalid_credentials(client: TestClient):
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()


def test_login_wrong_password(client: TestClient, test_user_data):
    client.post("/api/auth/register", json=test_user_data)

    login_data = {
        "email": test_user_data["email"],
        "password": "wrongpassword"
    }
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 401
