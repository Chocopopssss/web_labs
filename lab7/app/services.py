from fastapi import HTTPException, status
from app.repository import UserRepository, PostRepository, ConcurrentModificationError
from app.schemas import UserCreate, UserUpdate, PostCreate
from app.security import get_password_hash, verify_password, create_access_token
from app.models import User, Post


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
        return self.repo.create_with_optional_post(
            name=user_data.name,
            email=user_data.email,
            age=user_data.age,
            hashed_password=hashed_pw,
            bio=user_data.bio or "",
            welcome_title=user_data.welcome_post_title,
            welcome_content=user_data.welcome_post_content,
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
        try:
            return self.repo.update(current_user, user_data)
        except ConcurrentModificationError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(exc)
            )

    def delete_profile(self, current_user: User) -> None:
        self.repo.delete(current_user)


class PostService:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    def create_post(self, user_id: int, post_data: PostCreate) -> Post:
        return self.repo.create_post(user_id, post_data)

    def list_posts(self, optimized: bool = True) -> tuple[str, list[dict]]:
        if optimized:
            return "joinedload (1 JOIN query)", self.repo.get_posts_optimized()
        return "N+1 (separate query per author)", self.repo.get_posts_n_plus_one()

    def analyze_explain(self, sql_query: str) -> tuple[float, list[dict]]:
        allowed_prefixes = ("SELECT ",)
        normalized = sql_query.strip().upper()
        if not normalized.startswith(allowed_prefixes):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only SELECT queries are allowed for EXPLAIN QUERY PLAN"
            )
        return self.repo.explain_query(sql_query)
