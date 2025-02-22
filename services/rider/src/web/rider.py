from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import APIKeyHeader
from typing import List

from src.service import rider as rider_service
from src.model import rider as schemas
from error import RiderError
from src.service.security import get_current_user

router = APIRouter(prefix="/riders")

api_key_header = APIKeyHeader(name="Authorization", auto_error=False, scheme_name="Bearer")

async def get_current_user_multi(authorization: str = Depends(api_key_header)) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.strip()
    if not token.lower().startswith("bearer "):
        token = f"Bearer {token}"
    return await get_current_user(token)

@router.post("/", response_model=schemas.RiderResponse, status_code=201)
def create_rider(rider: schemas.RiderCreate):
    return rider_service.create_rider(rider)

@router.get("/me", response_model=schemas.RiderResponse)
async def read_riders_me(current_user: str = Depends(get_current_user_multi)):
    rider = rider_service.get_rider_by_username(current_user)
    if not rider:
        raise RiderError.RIDER_NOT_FOUND
    return rider

@router.get("/{rider_id}", response_model=schemas.RiderResponse)
def read_rider(rider_id: int, current_user: str = Depends(get_current_user_multi)):
    db_rider = rider_service.get_rider(rider_id)
    if not db_rider:
        raise RiderError.RIDER_NOT_FOUND
    return db_rider

@router.get("/", response_model=List[schemas.RiderResponse])
def read_riders(skip: int = 0, limit: int = 100):
    return rider_service.get_riders(skip=skip, limit=limit)

@router.put("/{rider_id}", response_model=schemas.RiderResponse)
def update_rider(rider_id: int, rider: schemas.RiderUpdate, current_user: str = Depends(get_current_user_multi)):
    db_rider = rider_service.get_rider(rider_id)
    if not db_rider:
        raise RiderError.RIDER_NOT_FOUND
    if db_rider.username != current_user:
        raise RiderError.PERMISSION_DENIED
    return rider_service.update_rider(rider_id, rider)

@router.delete("/{rider_id}", status_code=204)
def delete_rider(rider_id: int, current_user: str = Depends(get_current_user_multi)):
    db_rider = rider_service.get_rider(rider_id)
    if not db_rider:
        raise RiderError.RIDER_NOT_FOUND
    if db_rider.username != current_user:
        raise RiderError.PERMISSION_DENIED
    rider_service.delete_rider(rider_id)
    return None
