import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def test_user_data():
    return {
        "email": "testuser@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }


@pytest.fixture
def test_admin_data():
    return {
        "email": "admin@example.com",
        "password": "adminpassword123",
        "full_name": "Admin User"
    }


@pytest.fixture
def test_sweet_data():
    return {
        "name": "Test Chocolate",
        "description": "Delicious test chocolate",
        "category": "chocolate",
        "price": 3.99,
        "quantity": 50,
        "image_url": "https://example.com/chocolate.jpg"
    }
