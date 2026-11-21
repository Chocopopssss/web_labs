import time
from sqlalchemy import text
from sqlalchemy.orm import Session, joinedload
from app.models import User, Post
from app.schemas import UserUpdate, PostCreate


class ConcurrentModificationError(Exception):
    pass


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_all(self) -> list[User]:
        return self.db.query(User).all()

    def create_with_optional_post(
        self,
        name: str,
        email: str,
        age: int,
        hashed_password: str,
        bio: str = "",
        welcome_title: str | None = None,
        welcome_content: str | None = None,
    ) -> User:
        try:
            db_user = User(
                name=name,
                email=email,
                age=age,
                hashed_password=hashed_password,
                bio=bio,
                version=1,
            )
            self.db.add(db_user)
            self.db.flush()  # получаем db_user.id до коммита

            if welcome_title and welcome_content:
                post = Post(
                    title=welcome_title,
                    content=welcome_content,
                    user_id=db_user.id,
                )
                self.db.add(post)

            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except Exception:
            self.db.rollback()
            raise

    def update(self, user: User, user_data: UserUpdate) -> User:
        update_dict = user_data.model_dump(exclude_unset=True)
        expected_version = update_dict.pop("version", None)

        if expected_version is not None and user.version != expected_version:
            raise ConcurrentModificationError(
                f"Version conflict: expected {expected_version}, current is {user.version}"
            )

        try:
            for key, value in update_dict.items():
                setattr(user, key, value)
            user.version = (user.version or 1) + 1
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception:
            self.db.rollback()
            raise

    def delete(self, user: User) -> None:
        try:
            self.db.delete(user)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_post(self, user_id: int, post_data: PostCreate) -> Post:
        try:
            post = Post(
                title=post_data.title,
                content=post_data.content,
                user_id=user_id,
            )
            self.db.add(post)
            self.db.commit()
            self.db.refresh(post)
            return post
        except Exception:
            self.db.rollback()
            raise

    def get_posts_n_plus_one(self) -> list[dict]:
        """Намеренно читает автора отдельным запросом для каждого поста (N+1)."""
        posts = self.db.query(Post).all()
        result = []
        for p in posts:
            author = self.db.query(User).filter(User.id == p.user_id).first()
            result.append({
                "id": p.id,
                "title": p.title,
                "content": p.content,
                "user_id": p.user_id,
                "author_name": author.name if author else "",
                "author_email": author.email if author else "",
            })
        return result

    def get_posts_optimized(self) -> list[dict]:
        """Загружает посты вместе с авторами одним JOIN-запросом."""
        posts = self.db.query(Post).options(joinedload(Post.author)).all()
        return [
            {
                "id": p.id,
                "title": p.title,
                "content": p.content,
                "user_id": p.user_id,
                "author_name": p.author.name if p.author else "",
                "author_email": p.author.email if p.author else "",
            }
            for p in posts
        ]

    def explain_query(self, raw_sql: str) -> tuple[float, list[dict]]:
        start = time.perf_counter()
        rows = self.db.execute(text(f"EXPLAIN QUERY PLAN {raw_sql}")).fetchall()
        elapsed_ms = (time.perf_counter() - start) * 1000
        plan = [dict(row._mapping) for row in rows]
        return round(elapsed_ms, 3), plan
