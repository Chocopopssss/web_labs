from fastapi import HTTPException, status
from app.repository import UserRepository
from app.schemas import UserCreate, UserUpdate

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_users(self):
        return self.repository.get_all()

    def get_user(self, user_id: int):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        return user

    def create_user(self, user_data: UserCreate):
        # Бизнес-проверка: занят ли email
        existing_user = self.repository.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        return self.repository.create(user_data.model_dump())

    def update_user(self, user_id: int, user_data: UserUpdate):
        # Проверяем, существует ли пользователь
        self.get_user(user_id)
        
        # Если меняется email, проверяем его уникальность
        if user_data.email:
            existing_user = self.repository.get_by_email(user_data.email)
            if existing_user and existing_user["id"] != user_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered"
                )
                
        updated_user = self.repository.update(user_id, user_data.model_dump(exclude_unset=True))
        return updated_user

    def delete_user(self, user_id: int):
        # Проверяем, существует ли пользователь перед удалением
        self.get_user(user_id)
        return self.repository.delete(user_id)
