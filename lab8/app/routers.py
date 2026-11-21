from fastapi import APIRouter, Depends, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.repository import UserRepository, PostRepository
from app.services import UserService, PostService
from app.schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    Token,
    PostCreate,
    PostsQueryReport,
    ExplainPlanResponse,
)
from app.security import get_current_user
from app.models import User

auth_router = APIRouter(prefix="/auth", tags=["Auth"])
users_router = APIRouter(prefix="/users", tags=["Users & Profiles"])
posts_router = APIRouter(prefix="/posts", tags=["Posts & Optimization"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


def get_post_service(db: Session = Depends(get_db)) -> PostService:
    return PostService(PostRepository(db))


@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, service: UserService = Depends(get_user_service)):
    return service.register_user(user_data)


@auth_router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), service: UserService = Depends(get_user_service)):
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


@posts_router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    service: PostService = Depends(get_post_service)
):
    post = service.create_post(current_user.id, post_data)
    return {"id": post.id, "title": post.title, "content": post.content, "user_id": post.user_id}


@posts_router.put("/{post_id}")
def update_post(
    post_id: int,
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    service: PostService = Depends(get_post_service)
):
    post = service.update_post(post_id, current_user.id, post_data)
    return {"id": post.id, "title": post.title, "content": post.content, "user_id": post.user_id}


@posts_router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    service: PostService = Depends(get_post_service)
):
    service.delete_post(post_id, current_user.id)
    return None


@posts_router.get("/", response_model=PostsQueryReport)
def list_posts(
    optimized: bool = Query(default=True, description="True = joinedload, False = N+1"),
    db: Session = Depends(get_db),
    service: PostService = Depends(get_post_service)
):
    db.connection().info["query_count"] = 0
    strategy, items = service.list_posts(optimized=optimized)
    count = db.connection().info.get("query_count", 0)
    return {
        "strategy": strategy,
        "sql_queries_executed": count,
        "items": items,
    }


@posts_router.get("/explain", response_model=ExplainPlanResponse)
def explain_sql(
    sql: str = Query(
        default="SELECT * FROM users WHERE age > 18",
        description="SELECT-запрос для анализа через EXPLAIN QUERY PLAN"
    ),
    service: PostService = Depends(get_post_service)
):
    elapsed_ms, plan = service.analyze_explain(sql)
    return {
        "query": sql,
        "execution_time_ms": elapsed_ms,
        "plan": plan,
    }
