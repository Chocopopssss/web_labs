from fastapi import APIRouter, Depends, status
from app.repository import UserRepository
from app.services import UserService
from app.schemas import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

# Создаем единственный экземпляр репозитория (singleton в памяти)
user_repository = UserRepository()

def get_user_service() -> UserService:
    return UserService(user_repository)

@router.get("/", response_model=list[UserResponse])
def get_users(service: UserService = Depends(get_user_service)):
    return service.get_users()

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    return service.get_user(user_id)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create_user(user_data)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, service: UserService = Depends(get_user_service)):
    return service.update_user(user_id, user_data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    service.delete_user(user_id)
    return None
