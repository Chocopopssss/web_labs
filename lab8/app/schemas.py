from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(..., ge=0, le=120)
    password: str = Field(..., min_length=6)
    bio: str | None = Field(default="", max_length=255)
    welcome_post_title: str | None = Field(default=None, max_length=120)
    welcome_post_content: str | None = Field(default=None, max_length=1000)


class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=50)
    age: int | None = Field(None, ge=0, le=120)
    bio: str | None = Field(None, max_length=255)
    version: int | None = Field(
        default=None,
        description="Текущая версия записи для защиты от конкурентных изменений"
    )


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    bio: str | None = ""
    version: int = 1

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    content: str = Field(..., min_length=1)


class PostWithAuthorResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    author_name: str
    author_email: str


class PostsQueryReport(BaseModel):
    strategy: str
    sql_queries_executed: int
    items: list[PostWithAuthorResponse]


class ExplainPlanResponse(BaseModel):
    query: str
    execution_time_ms: float
    plan: list[dict]
