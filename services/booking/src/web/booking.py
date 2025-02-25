
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import APIKeyHeader
from typing import List

from src.service import booking as booking_service
from src.model import booking as schemas
from src.service.security import get_current_booking
from src.error import BookingError
from src.service.booking import calculate_fare

# Router for CRUD endpoints with prefix "/bookings"
router = APIRouter(prefix="/bookings")

api_key_header = APIKeyHeader(name="Authorization", auto_error=False, scheme_name="Bearer")

async def get_current_booking_multi(authorization: str = Depends(api_key_header)) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.strip()
    if not token.lower().startswith("bearer "):
        token = f"Bearer {token}"
    return await get_current_booking(token)

@router.post("/", response_model=schemas.BookingResponse, status_code=201)
def create_booking(booking: schemas.BookingCreate):
    return booking_service.create_booking(booking)

@router.get("/{booking_id}", response_model=schemas.BookingResponse)
def get_booking(booking_id: int):
    return booking_service.get_booking(booking_id)

@router.put("/{booking_id}/status", response_model=schemas.BookingResponse)
def update_booking_status(booking_id: int, status: schemas.BookingUpdate):
    return booking_service.update_booking_status(booking_id, status.status)


#tự động gán tài xế và tính giá cước:
@router.post("/", response_model=schemas.BookingResponse)
def create_booking(booking: schemas.BookingCreate):
    booking.fare = calculate_fare(booking.distance)
    nearest_rider = find_nearest_rider(booking.pickup_location)
    if not nearest_rider:
        raise HTTPException(status_code=400, detail="No available riders")
    booking.rider_id = nearest_rider.id
    return booking_service.create_booking(booking)

#cập nhập trạng thái di chuyển
@router.put("/{booking_id}/status", response_model=schemas.BookingResponse)
def update_status(booking_id: int, status: str):
    return booking_service.update_booking_status(booking_id, status)