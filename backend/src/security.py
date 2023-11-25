from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.authentication import AuthCredentials, UnauthenticatedUser

from src.config import settings
from src.database.database import get_db
from src.models.users import Users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/sign_in")

credentials_error = HTTPException(
    status_code=400,
    detail="Invalid Login Credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def create_access_token(data, expiry: timedelta):
    payload = data.copy()
    expire_in = datetime.utcnow() + expiry
    payload.update({"exp": expire_in})
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


async def create_refresh_token(data, expiry):
    payload = data.copy()
    expire_in = datetime.utcnow() + expiry
    payload.update({"exp": expire_in})
    return jwt.encode(data, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def get_token_payload(token):
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError:
        return None
    return payload


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> Users | None:
    payload = get_token_payload(token)
    if not payload or not isinstance(payload, dict):
        raise credentials_error

    user_id: int | None = payload.get("id", None)

    if not user_id:
        raise credentials_error

    user = await db.execute(select(Users).where(Users.id == user_id))
    user = user.first()
    user = user[0]
    return user


async def get_current_admin(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> Users | None:
    user = await get_current_user(token, db)
    if not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="You are not an admin.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


class JWTAuth:
    async def authenticate(self, conn):
        guest = AuthCredentials(["unauthenticated"]), UnauthenticatedUser()

        if "authorization" not in conn.headers:
            return guest

        token = conn.headers.get("authorization").split(" ")[1]
        if not token:
            return guest

        user = get_current_user(token=token)

        if not user:
            return guest

        return AuthCredentials("authenticated"), user
