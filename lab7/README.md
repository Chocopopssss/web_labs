# Лабораторная работа №7. Транзакции и оптимизация запросов

REST API сервис управления пользователями и постами на **FastAPI**, **SQLAlchemy**, **SQLite**, **Alembic**, **JWT** и **Docker Compose** с реализацией транзакций, оптимистичной блокировки, индексов, устранения проблемы N+1 и анализа планов запросов.

## Реализованные задачи

* **Использование транзакций** — атомарное создание пользователя и стартового поста в одной транзакции (`flush` / `commit` / `rollback` при ошибке).
* **Обработка конкурентных изменений** — оптимистичная блокировка через поле `version` в модели `User` с возвратом `409 Conflict` при несовпадении версии.
* **Добавление индексов** — индекс по `users.age`, индекс по `posts.user_id` и составной индекс по `posts(user_id, id)`, применённые через миграцию Alembic.
* **Оптимизация N+1 проблемы** — сравнение «наивного» получения постов с авторами (`N+1` запросов) и оптимизированного запроса через `joinedload(Post.author)` с подсчётом SQL-запросов.
* **Анализ медленных запросов** — профилирование SQL-запросов и эндпоинт `GET /posts/explain` для просмотра `EXPLAIN QUERY PLAN` и времени выполнения.

## Структура проекта

```text
lab7/
├── alembic/
│   ├── versions/
│   └── env.py
├── app/
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── repository.py
│   ├── services.py
│   └── routers.py
├── screenshots/
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── main.py
└── requirements.txt
```

## Запуск проекта

1. Сборка образа:
   ```bash
   docker compose build
   ```
2. Применение миграций:
   ```bash
   docker compose run --rm api alembic upgrade head
   ```
3. Запуск сервиса:
   ```bash
   docker compose up
   ```

Swagger UI доступен по адресу: `http://localhost:8000/docs`

Остановка контейнеров:
```bash
docker compose down
```

## Основные эндпоинты

* `POST /auth/register` — регистрация пользователя (опционально со стартовым постом в одной транзакции, статус `201`)
* `POST /auth/login` — получение JWT-токена
* `GET /users/me` — получение текущего профиля (включая `version`)
* `PUT /users/me` — обновление профиля с проверкой `version` (`200` при актуальной версии, `409` при конфликте)
* `GET /users/` — список пользователей
* `DELETE /users/me` — удаление профиля (`204`)
* `POST /posts/` — создание поста авторизованным пользователем (`201`)
* `GET /posts/?optimized=true|false` — получение постов с авторами (`joinedload` или `N+1`) и количеством SQL-запросов
* `GET /posts/explain` — выполнение `EXPLAIN QUERY PLAN` и замер времени запроса

## Скриншоты (`screenshots/`)

1. `01_migration_and_run.png` — применение миграции Alembic и запуск Uvicorn в Docker
2. `02_transaction_register_201.png` — транзакционная регистрация (`POST /auth/register`, `201`)
3. `03_optimistic_lock_409.png` — конфликт версий при конкурентном обновлении (`PUT /users/me`, `409`)
4. `04_n_plus_one_vs_joinedload.png` — сравнение N+1 и `joinedload` (`GET /posts/`)
5. `05_explain_query_plan.png` — план выполнения и время запроса (`GET /posts/explain`)