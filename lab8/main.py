from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth_router, users_router, posts_router

app = FastAPI(title="Lab 8 - Nginx Reverse Proxy & Security")

origins = [
    "https://localhost",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(posts_router)


@app.get("/")
def root():
    return {"message": "Lab 8 API is running behind Nginx!"}
