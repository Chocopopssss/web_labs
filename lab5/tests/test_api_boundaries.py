from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user_invalid_age_negative():
    # Граничный/ошибочный тест: возраст меньше 0
    response = client.post(
        "/users/",
        json={"name": "Tom", "email": "tom@example.com", "age": -5}
    )
    assert response.status_code == 422  # Ошибка валидации Pydantic

def test_create_user_invalid_age_too_old():
    # Граничный/ошибочный тест: возраст больше 120
    response = client.post(
        "/users/",
        json={"name": "Grandpa", "email": "grandpa@example.com", "age": 150}
    )
    assert response.status_code == 422

def test_create_user_invalid_name_short():
    # Граничный тест: слишком короткое имя (min_length=2)
    response = client.post(
        "/users/",
        json={"name": "A", "email": "a@example.com", "age": 20}
    )
    assert response.status_code == 422
