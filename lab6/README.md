# Лабораторная работа №6. Работа с базами данных, миграциями, JWT-авторизацией и Docker

REST API сервис управления профилями пользователей, реализованный на **FastAPI** с использованием **SQLAlchemy**, **Alembic**, **JWT-авторизации** и контейнеризации через **Docker Compose**.

## Стек технологий

* **Python 3.11**
* **FastAPI** + **Uvicorn**
* **SQLAlchemy** + **SQLite**
* **Alembic** (миграции базы данных)
* **JWT** (OAuth2 Bearer) + **bcrypt** (хеширование паролей)
* **Docker** & **Docker Compose**

## Структура проекта

```text
lab6/
├── alembic/                 # Конфигурация и версии миграций Alembic
│   ├── versions/            # Сгенерированные скрипты миграций
│   └── env.py
├── app/                     # Основной пакет приложения
│   ├── database.py          # Подключение к БД и сессии SQLAlchemy
│   ├── models.py            # ORM-модель пользователя
│   ├── schemas.py           # Pydantic-схемы валидации и ответов
│   ├── security.py          # Хеширование паролей и работа с JWT-токенами
│   ├── repository.py        # Слой работы с базой данных (CRUD)
│   ├── services.py          # Бизнес-логика
│   └── routers.py           # Маршруты API (авторизация и пользователи)
├── screenshots/             # Скриншоты работы приложения для отчёта
├── alembic.ini              # Настройки Alembic
├── Dockerfile               # Инструкция сборки образа API
├── docker-compose.yml       # Конфигурация запуска контейнера
├── main.py                  # Точка входа FastAPI приложения
└── requirements.txt         # Зависимости проекта
```

## Запуск проекта в Docker

1. **Сборка Docker-образа:**
   ```bash
   docker compose build
   ```

2. **Применение миграций базы данных:**
   ```bash
   docker compose run --rm api alembic upgrade head
   ```

3. **Запуск сервиса:**
   ```bash
   docker compose up
   ```

После запуска интерактивная документация Swagger UI доступна по адресу:
`http://localhost:8000/docs`

Для остановки контейнеров выполните:
```bash
docker compose down
```

## Эндпоинты API

### Авторизация (`/auth`)
* `POST /auth/register` — регистрация нового пользователя (валидация полей, хеширование пароля, возврат статуса `201`).
* `POST /auth/login` (OAuth2) — аутентификация по `email` и паролю с выдачей JWT-токена.

### Пользователи и профили (`/users`)
* `GET /users/me` — получение профиля текущего авторизованного пользователя (требуется `Bearer` токен).
* `PUT /users/me` — обновление данных текущего пользователя (`name`, `age`, `bio`).
* `GET /users/` — получение списка всех пользователей.
* `DELETE /users/me` — удаление профиля текущего пользователя (возвращает статус `204`).

## Скриншоты (`screenshots/`)

1. `01_alembic_and_run.png` — миграция Alembic и запуск сервера
2. `02_register_201.png` — регистрация пользователя (`POST /auth/register`, `201`)
3. `03_profile_get_200.png` — получение профиля по JWT (`GET /users/me`, `200`)
4. `04_profile_update_200.png` — обновление профиля (`PUT /users/me`, `200`)
5. `05_profile_delete_204.png` — удаление профиля (`DELETE /users/me`, `204`)
