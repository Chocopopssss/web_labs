import logging
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Lab 3 REST API",
    description="API с расширенной валидацией, бизнес-правилами и обработкой ошибок",
    version="1.0.0",
)

# Хранилище в памяти
fake_users_db = []


# Pydantic схемы с валидацией
class UserCreate(BaseModel):
  name: str = Field(
      ..., min_length=2, max_length=50, description="Имя пользователя"
  )
  email: EmailStr = Field(..., description="Уникальный email")
  age: int | None = Field(
      None, ge=0, le=120, description="Возраст от 0 до 120 лет"
  )


class UserUpdate(BaseModel):
  name: str | None = Field(None, min_length=2, max_length=50)
  email: EmailStr | None = None
  age: int | None = Field(None, ge=0, le=120)


class User(BaseModel):
  id: int
  name: str
  email: str
  age: int | None = None


@app.post(
    "/users/", response_model=User, status_code=status.HTTP_201_CREATED
)
def create_user(user_data: UserCreate):
  logger.info(f"Попытка создания пользователя с email: {user_data.email}")

  # Бизнес-правило: проверка на уникальность email
  if any(u["email"] == user_data.email for u in fake_users_db):
    logger.warning(
        f"Ошибка бизнес-логики: email {user_data.email} уже занят."
    )
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="User with this email already exists",
    )

  new_id = len(fake_users_db) + 1
  user_dict = user_data.model_dump()
  user_dict["id"] = new_id
  fake_users_db.append(user_dict)

  logger.info(f"Пользователь успешно создан с ID: {new_id}")
  return user_dict


@app.get("/users/", response_model=list[User])
def get_users():
  logger.info("Запрос списка всех пользователей")
  return fake_users_db


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
  logger.info(f"Запрос пользователя с ID: {user_id}")
  user = next((u for u in fake_users_db if u["id"] == user_id), None)
  if not user:
    logger.error(f"Пользователь с ID {user_id} не найден (404)")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    )
  return user


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_data: UserUpdate):
  logger.info(f"Запрос на обновление пользователя с ID: {user_id}")
  user = next((u for u in fake_users_db if u["id"] == user_id), None)
  if not user:
    logger.error(
        f"Попытка обновить несуществующего пользователя с ID {user_id}"
    )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    )

  update_data = user_data.model_dump(exclude_unset=True)

  # Бизнес-правило: если меняют email, проверяем его уникальность
  if "email" in update_data:
    if any(
        u["email"] == update_data["email"] and u["id"] != user_id
        for u in fake_users_db
    ):
      logger.warning(
          f"Ошибка бизнес-логики: email {update_data['email']} уже занят другим"
          " пользователем."
      )
      raise HTTPException(
          status_code=status.HTTP_409_CONFLICT,
          detail="User with this email already exists",
      )

  user.update(update_data)
  logger.info(f"Пользователь с ID {user_id} успешно обновлен")
  return user


@app.delete(
    "/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(user_id: int):
  logger.info(f"Запрос на удаление пользователя с ID: {user_id}")
  global fake_users_db
  user = next((u for u in fake_users_db if u["id"] == user_id), None)
  if not user:
    logger.error(
        f"Попытка удалить несуществующего пользователя с ID {user_id}"
    )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    )

  fake_users_db = [u for u in fake_users_db if u["id"] != user_id]
  logger.info(f"Пользователь с ID {user_id} удален")
  return None
