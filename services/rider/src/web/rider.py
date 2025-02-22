from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, APIKeyHeader
from datetime import timedelta
from src.service import rider as rider_service
from src.model import rider as schemas
from src.service.security import create_access_token, get_current_rider, ACCESS_TOKEN_EXPIRE_MINUTES
from error import RiderError

router = APIRouter(prefix="/riders")
auth_router = APIRouter()

api_key_header = APIKeyHeader(name="Authorization", auto_error=False, scheme_name="Bearer")

async def get_current_rider_multi(authorization: str = Depends(api_key_header)) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.strip()
    if not token.lower().startswith("bearer "):
        token = f"Bearer {token}"
    return await get_current_rider(token)

@auth_router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        rider = rider_service.authenticate_rider(form_data.username, form_data.password)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": rider.username}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer", "message": "Authorization successful"}
    except Exception as e:
        raise RiderError.INVALID_CREDENTIALS

@auth_router.get("/auth/status")
def auth_status(current_rider: str = Depends(get_current_rider_multi)):
    rider = rider_service.get_rider_by_username(current_rider)
    if not rider:
        raise HTTPException(status_code=401, detail="Rider not found, please log in again")
    return {"message": "You have been successfully authorized", "username": current_rider}

