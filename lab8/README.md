# Лабораторная работа №8. Nginx reverse proxy и безопасность

REST API сервис на **FastAPI**, **SQLAlchemy**, **SQLite**, **Nginx** и **Docker Compose**, настроенный за обратным прокси с поддержкой HTTPS, редиректом HTTP -> HTTPS, раздачей статики и усиленной защитой приложения (CORS, контроль прав доступа к ресурсам и защита от SQL-инъекций).

## Реализованные задачи

* **Nginx reverse proxy и HTTPS** — проксирование трафика через Nginx на FastAPI (`api:8000`), подключение самоподписанного SSL-сертификата (`selfsigned.crt` / `selfsigned.key`) и автоматический редирект с порта `80` на `443`.
* **Раздача статических файлов через Nginx** — отдача файлов из `/static/` напрямую веб-сервером Nginx (`https://localhost/static/info.txt`).
* **Настройка CORS** — подключение `CORSMiddleware` в FastAPI с явным списком разрешённых источников (`allow_origins`), методов и заголовков.
* **Проверка прав доступа к постам** — контроль владельца записи (`post.user_id == current_user.id`) при изменении (`PUT /posts/{post_id}`) и удалении (`DELETE /posts/{post_id}`) постов с возвратом `403 Forbidden` при попытке изменить чужой пост.
* **Защита от SQL-инъекций** — валидация SQL-запроса перед передачей в `EXPLAIN QUERY PLAN` (`GET /posts/explain`): разрешены только безопасные `SELECT`-запросы без комментариев, множественных инструкций (`;`) и опасных SQL-ключевых слов (при нарушении возвращается `400 Bad Request`).

## Структура проекта
```text
lab8/
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
├── nginx/
│   ├── certs/
│   │   ├── selfsigned.crt
│   │   └── selfsigned.key
│   └── nginx.conf
├── screenshots/
│   ├── 01_static_https.png
│   ├── 02_forbidden_post_403.png
│   └── 03_sqli_blocked_400.png
├── static/
│   └── info.txt
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── lab8.db
├── main.py
├── README.md
└── requirements.txt

## Запуск проекта

1. Генерация самоподписанного SSL-сертификата в `nginx/certs/`:
   docker run --rm -v "%cd%\nginx\certs:/etc/nginx/certs" alpine/openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/certs/selfsigned.key -out /etc/nginx/certs/selfsigned.crt -subj "/CN=localhost"

2. Сборка и запуск сервисов (`api` и `nginx`):
   docker compose up --build

3. Инициализация таблиц базы данных:
   docker compose exec api python -c "from app.database import Base, engine; import app.models; Base.metadata.create_all(bind=engine); print('Tables created!')"

Статический файл по HTTPS: https://localhost/static/info.txt
Swagger UI через Nginx: https://localhost/docs

Остановка контейнеров:
docker compose down

## Основные эндпоинты

* `POST /auth/register` — регистрация пользователя (статус `201`)
* `POST /auth/login` — получение JWT-токена
* `GET /users/me` — получение текущего профиля
* `PUT /users/me` — обновление профиля
* `GET /users/` — список пользователей
* `DELETE /users/me` — удаление профиля (`204`)
* `POST /posts/` — создание поста авторизованным пользователем (`201`)
* `PUT /posts/{post_id}` — обновление поста (`200` для автора, `403` при попытке изменить чужой пост)
* `DELETE /posts/{post_id}` — удаление поста (`204` для автора, `403` при попытке удалить чужой пост)
* `GET /posts/?optimized=true|false` — получение постов с авторами (`joinedload` или `N+1`) и количеством SQL-запросов
* `GET /posts/explain` — выполнение `EXPLAIN QUERY PLAN` с проверкой безопасности запроса (`200` или `400` при опасном SQL)

## Скриншоты (`screenshots/`)

1. `01_static_https.png` — отдача статического файла по HTTPS через Nginx (`https://localhost/static/info.txt`)
2. `02_forbidden_post_403.png` — отказ в доступе при попытке изменить чужой пост (`PUT /posts/1`, `403 Forbidden`)
3. `03_sqli_blocked_400.png` — блокировка опасного SQL-запроса в `GET /posts/explain` (`400 Bad Request`)
