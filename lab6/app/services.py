from fastapi import HTTPException, status
from app.repository import UserRepository
from app.schemas import UserCreate, UserUpdate
from app.security import get_password_hash, verify_password, create_access_token
from app.models import User

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register_user(self, user_data: UserCreate) -> User:
        if self.repo.get_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        hashed_pw = get_password_hash(user_data.password)
        return self.repo.create(
            name=user_data.name,
            email=user_data.email,
            age=user_data.age,
            hashed_password=hashed_pw,
            bio=user_data.bio or ""
        )

    def authenticate_user(self, email: str, password: str) -> str:
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return create_access_token(data={"sub": user.email})

    def get_users(self) -> list[User]:
        return self.repo.get_all()

    def update_profile(self, current_user: User, user_data: UserUpdate) -> User:
        return self.repo.update(current_user, user_data)

    def delete_profile(self, current_user: User) -> None:
        self.repo.delete(current_user)
