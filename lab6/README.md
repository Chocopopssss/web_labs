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
* `GET /users/` — получение списка всех пользователей[cite: 13].
* `DELETE /users/me` — удаление профиля текущего пользователя (возвращает статус `204`).

## Скриншоты тестирования

В папке `screenshots/` представлены результаты сборки, миграций и тестирования всех эндпоинтов через Swagger UI:

1. `01_docker_build.png` — успешная сборка образа `lab6-api`.
2. `02_alembic_upgrade.png` — применение миграции `Initial users table`.
3. `03_docker_up.png` — запуск сервера Uvicorn внутри контейнера.
4. `04_swagger_overview.png` — общий интерфейс документации Swagger UI.
5. `05_register_201.png` — регистрация пользователя (`POST /auth/register`, код `201`).
6. `06_users_me_get_200.png` — получение профиля с JWT-токеном (`GET /users/me`, код `200`).
7. `07_users_me_put_200.png` — обновление данных профиля (`PUT /users/me`, код `200`).
8. `08_users_list_200.png` — просмотр списка пользователей (`GET /users/`, код `200`).
9. `09_users_me_delete_204.png` — удаление профиля (`DELETE /users/me`, код `204`).
