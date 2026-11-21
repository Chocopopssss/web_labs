from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserUpdate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_all(self) -> list[User]:
        return self.db.query(User).all()

    def create(self, name: str, email: str, age: int, hashed_password: str, bio: str = "") -> User:
        db_user = User(
            name=name,
            email=email,
            age=age,
            hashed_password=hashed_password,
            bio=bio
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user: User, user_data: UserUpdate) -> User:
        update_dict = user_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
