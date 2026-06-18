from pydantic import BaseModel, EmailStr

from app.constants.enums import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    role: UserRole = UserRole.STUDENT


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: UserRole
    bio: str | None = None

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
