from fastapi import FastAPI
from app.routers import router as users_router

app = FastAPI(
    title="Lab 4 Clean Architecture API",
    description="API с разделением на слои (Handler, Service, Repository) и Dependency Injection",
    version="1.0.0"
)

# Подключаем роутер пользователей
app.include_router(users_router)

@app.get("/")
def root():
    return {"message": "Welcome to Lab 4. Go to /docs for Swagger UI."}
