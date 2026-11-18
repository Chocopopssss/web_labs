from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(..., ge=0, le=120)

class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=50)
    email: EmailStr | None = None
    age: int | None = Field(None, ge=0, le=120)

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int

    class Config:
        from_attributes = True
