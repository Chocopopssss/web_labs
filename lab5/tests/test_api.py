from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_create_user():
    response = client.post(
        "/users/",
        json={"name": "Alice", "email": "alice@example.com", "age": 25}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert data["age"] == 25
    assert "id" in data

def test_create_user_duplicate_email():
    # Создаем первого пользователя
    client.post(
        "/users/",
        json={"name": "Bob", "email": "bob@example.com", "age": 30}
    )
    # Пытаемся создать с тем же email
    response = client.post(
        "/users/",
        json={"name": "Bobby", "email": "bob@example.com", "age": 22}
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered"

def test_get_user_not_found():
    response = client.get("/users/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User with id 9999 not found"
