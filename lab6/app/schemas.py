from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(..., ge=0, le=120)
    password: str = Field(..., min_length=6)
    bio: str | None = Field(default="", max_length=255)

class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=50)
    age: int | None = Field(None, ge=0, le=120)
    bio: str | None = Field(None, max_length=255)

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    bio: str | None = ""

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
