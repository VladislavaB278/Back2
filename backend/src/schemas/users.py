from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    registered_at: datetime
    is_admin: bool


class UserSchema(UserRead):
    password: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int


class UserAdmin(BaseModel):
    id: int | None = None
    username: str | None = None
    email: EmailStr | None = None
    registered_at: datetime | None = None
    is_admin: bool | None = None
    password: int | None = None
