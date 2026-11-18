import pytest
from unittest.mock import MagicMock
from app.services import UserService
from app.schemas import UserCreate
from fastapi import HTTPException

def test_service_create_user_success():
    # Создаем mock-репозиторий
    mock_repo = MagicMock()
    mock_repo.get_by_email.return_value = None  # Пользователя с таким email еще нет
    # Имитируем сохранение в БД
    mock_repo.create.return_value = {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 25}

    service = UserService(mock_repo)
    user_data = UserCreate(name="Alice", email="alice@example.com", age=25)
    
    result = service.create_user(user_data)
    
    assert result["id"] == 1
    assert result["name"] == "Alice"
    mock_repo.create.assert_called_once()

def test_service_create_user_duplicate_email():
    mock_repo = MagicMock()
    # Имитируем, что пользователь с таким email уже существует
    mock_repo.get_by_email.return_value = {"id": 1, "name": "Bob", "email": "bob@example.com", "age": 30}

    service = UserService(mock_repo)
    user_data = UserCreate(name="Bobby", email="bob@example.com", age=22)

    with pytest.raises(HTTPException) as exc_info:
        service.create_user(user_data)
    
    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "Email already registered"
