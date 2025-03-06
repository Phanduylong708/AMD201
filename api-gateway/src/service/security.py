from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import os
from src.data.rider import get_rider_by_username 
# from src.data.user import get_user_by_username
from fastapi import HTTPException, Depends
from src.data.init import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer


rider_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8002/riders/login")
# user_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/gateway/login/user")


# Load environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set in environment variables")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    print(f"Authenticating user: {username}")  # 🔍 Debugging
    user = get_user_by_username(db, username)
    
    if not user:
        print("User not found!")
        raise HTTPException(status_code=400, detail="Invalid username or password")

    if not verify_password(password, user.hashed_password):
        print("Incorrect password!")
        raise HTTPException(status_code=400, detail="Invalid username or password")

    print("✅ User authentication successful!")
    return user


def authenticate_rider(username: str, password: str, db: Session = Depends(get_db)):
    print(f"Authenticating rider: {username}")  # 🔍 Debugging
    rider = get_rider_by_username(db, username)
    
    if not rider:
        print("Rider not found!")
        raise HTTPException(status_code=400, detail="Invalid username or password")

    if not verify_password(password, rider.hashed_password):
        print("Incorrect password!")
        raise HTTPException(status_code=400, detail="Invalid username or password")

    print("✅ Rider authentication successful!")
    return rider
