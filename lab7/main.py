from fastapi import FastAPI
from app.routers import auth_router, users_router, posts_router

app = FastAPI(title="Lab 7 - Transactions & Query Optimization")

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(posts_router)


@app.get("/")
def root():
    return {"message": "Lab 7 API is running!"}
