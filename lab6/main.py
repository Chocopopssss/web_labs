from fastapi import FastAPI
from app.routers import auth_router, users_router

app = FastAPI(title="Lab 6 Auth & Database API")

app.include_router(auth_router)
app.include_router(users_router)

@app.get("/")
def root():
    return {"message": "Lab 6 API is running!"}
