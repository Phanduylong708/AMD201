from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, APIKeyHeader
from datetime import timedelta
from typing import List

from src.service import user as user_service
from src.model import user as schemas
from src.service.security import create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from src.error import UserError

# Router for CRUD endpoints with prefix "/users"
router = APIRouter(prefix="/users")

api_key_header = APIKeyHeader(name="Authorization", auto_error=False, scheme_name="Bearer")

async def get_current_user_multi(authorization: str = Depends(api_key_header)) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.strip()
    if not token.lower().startswith("bearer "):
        token = f"Bearer {token}"
    return await get_current_user(token)

@router.post("/", response_model=schemas.UserResponse, status_code=201)
def create_user(user: schemas.UserCreate):
    try:
        return user_service.create_user(user)
    except ValueError as e:
        if "Password must be" in str(e):
            raise UserError.INVALID_PASSWORD
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me", response_model=schemas.UserResponse)
async def read_users_me(current_user: str = Depends(get_current_user_multi)):
    user = user_service.get_user_by_username(current_user)
    if not user:
        raise UserError.USER_NOT_FOUND
    return user

@router.get("/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, current_user: str = Depends(get_current_user_multi)):
    db_user = user_service.get_user(user_id)
    if not db_user:
        raise UserError.USER_NOT_FOUND
    return db_user

@router.get("/", response_model=List[schemas.UserResponse])
def read_users(skip: int = 0, limit: int = 100):
    return user_service.get_users(skip=skip, limit=limit)

# New router for authentication endpoints without prefix
auth_router = APIRouter()

@auth_router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = user_service.authenticate_user(form_data.username, form_data.password)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer", "message": "Authorization successful"}
    except Exception as e:
        raise UserError.INVALID_CREDENTIALS

@auth_router.get("/auth/status")
def auth_status(current_user: str = Depends(get_current_user_multi)):
    user = user_service.get_user_by_username(current_user)
    if not user:
        raise HTTPException(status_code=401, detail="User not found, please log in again")
    return {"message": "You have been successfully authorized", "username": current_user}

# New router for admin operations without using Bearer prefix
ADMIN_TOKEN = "admin_static_token"

def get_current_admin(authorization: str = Depends(api_key_header)) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.strip()
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Not authorized as admin")
    return "admin"

admin_router = APIRouter()

@admin_router.get("/users", response_model=List[schemas.UserResponse])
def admin_read_users(current_admin: str = Depends(get_current_admin)):
    return user_service.get_users(skip=0, limit=100)

@admin_router.get("/users/{user_id}", response_model=schemas.UserResponse)
def admin_read_user(user_id: int, current_admin: str = Depends(get_current_admin)):
    db_user = user_service.get_user(user_id)
    if not db_user:
        raise UserError.USER_NOT_FOUND
    return db_user

@admin_router.put("/users/{user_id}", response_model=schemas.UserResponse)
def admin_update_user(user_id: int, user: schemas.UserUpdate, current_admin: str = Depends(get_current_admin)):
    db_user = user_service.get_user(user_id)
    if not db_user:
        raise UserError.USER_NOT_FOUND
    return user_service.update_user(user_id, user)

@admin_router.delete("/users/{user_id}", status_code=200)
def admin_delete_user(user_id: int, current_admin: str = Depends(get_current_admin)):
    db_user = user_service.get_user(user_id)
    if not db_user:
        raise UserError.USER_NOT_FOUND
    user_service.delete_user(user_id)
    return {"message": "User deleted successfully"}

# New endpoint for self update for normal users
@router.put("/me", response_model=schemas.UserResponse)
def update_me(user: schemas.UserUpdate, current_user: str = Depends(get_current_user_multi)):
    db_user = user_service.get_user_by_username(current_user)
    if not db_user:
        raise UserError.USER_NOT_FOUND
    return user_service.update_user(db_user.id, user)

# New endpoint for self delete for normal users
@router.delete("/me", status_code=200)
def delete_me(current_user: str = Depends(get_current_user_multi)):
    user = user_service.get_user_by_username(current_user)
    if not user:
        raise UserError.USER_NOT_FOUND
    user_service.delete_user(user.id)
    return {"message": "User deleted successfully"}
