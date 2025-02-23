from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
from src.error import RiderError
from src.data.models import get_rider_by_username  #Import from data layer
import os
from dotenv import load_dotenv

#Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


#Use API Gateway for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8000/riders/login")

# 🔹 Load environment variables from `.env`
load_dotenv()

#Secret key & JWT settings (must match API Gateway)
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set in environment variables")

ALGORITHM = "HS256"
def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Generates a JWT token for authentication.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_rider(username: str, password: str):
    rider = get_rider_by_username(username)
    if not rider:
        raise RiderError.INVALID_CREDENTIALS  # Specific error message
    if not verify_password(password, rider.hashed_password):
        raise RiderError.INVALID_CREDENTIALS
    return rider

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Decodes JWT token and extracts the current rider's username.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"sub": username, "role": payload.get("role")}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
