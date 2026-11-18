from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Lab 2 REST API",
    description="CRUD API для управления пользователями",
    version="1.0.0"
)

# Pydantic-модели для валидации данных
class UserCreate(BaseModel):
    name: str
    email: str
    age: Optional[int] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None

class User(UserCreate):
    id: int

# Временное хранилище данных в памяти
fake_users_db = {}
id_counter = 1

# 1. CREATE (Создание пользователя) - Статус 201 Created
@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate):
    global id_counter
    new_user = User(id=id_counter, **user_data.dict())
    fake_users_db[id_counter] = new_user
    id_counter += 1
    return new_user

# 2. READ ALL (Получение списка пользователей) - Статус 200 OK
@app.get("/users/", response_model=List[User])
def get_users():
    return list(fake_users_db.values())

# 3. READ ONE (Получение одного пользователя по ID) - Статус 200 OK или 404
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return fake_users_db[user_id]

# 4. UPDATE (Обновление пользователя) - Статус 200 OK
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_data: UserUpdate):
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    stored_user = fake_users_db[user_id]
    update_data = user_data.dict(exclude_unset=True)
    
    updated_user = stored_user.copy(update=update_data)
    fake_users_db[user_id] = updated_user
    return updated_user

# 5. DELETE (Удаление пользователя) - Статус 204 No Content
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    del fake_users_db[user_id]
    return None
