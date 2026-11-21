from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.repository import UserRepository
from app.services import UserService
from app.schemas import UserCreate, UserUpdate, UserResponse, Token
from app.security import get_current_user
from app.models import User

auth_router = APIRouter(prefix="/auth", tags=["Auth"])
users_router = APIRouter(prefix="/users", tags=["Users & Profiles"])

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))

@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, service: UserService = Depends(get_user_service)):
    return service.register_user(user_data)

@auth_router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), service: UserService = Depends(get_user_service)):
    # OAuth2PasswordRequestForm передает email в поле username
    token = service.authenticate_user(form_data.username, form_data.password)
    return {"access_token": token, "token_type": "bearer"}

@users_router.get("/me", response_model=UserResponse)
def read_my_profile(current_user: User = Depends(get_current_user)):
    return current_user

@users_router.put("/me", response_model=UserResponse)
def update_my_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    return service.update_profile(current_user, user_data)

@users_router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_profile(
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    service.delete_profile(current_user)
    return None

@users_router.get("/", response_model=list[UserResponse])
def list_users(
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    return service.get_users()
