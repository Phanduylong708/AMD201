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
    return user_service.create_user(user)

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

@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserUpdate, current_user: str = Depends(get_current_user_multi)):
    db_user = user_service.get_user(user_id)
    if not db_user:
        raise UserError.USER_NOT_FOUND
    if db_user.username != current_user:
        raise UserError.PERMISSION_DENIED
    return user_service.update_user(user_id, user)

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, current_user: str = Depends(get_current_user_multi)):
    db_user = user_service.get_user(user_id)
    if not db_user:
        raise UserError.USER_NOT_FOUND
    if db_user.username != current_user:
        raise UserError.PERMISSION_DENIED
    user_service.delete_user(user_id)
    return None

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
