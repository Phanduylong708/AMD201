from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

from src.error import UserError

# Configuration: SECRET_KEY should be set as an environment variable.
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set in environment variables")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str) -> str:
    if not token:
        raise UserError.INVALID_TOKEN
    token = token.strip()
    if not token.lower().startswith("bearer "):
        raise UserError.INVALID_TOKEN
    token = token[7:].strip()
    if not token:
        raise UserError.INVALID_TOKEN
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise UserError.INVALID_TOKEN
    except JWTError as e:
        raise UserError.INVALID_TOKEN
    username: str = payload.get("sub")
    if not username:
        raise UserError.INVALID_TOKEN
    return username 