from sqlalchemy.orm import Session 
from fastapi import APIRouter
from src.model import rider as schemas
from src.data import rider as data_rider

router = APIRouter(prefix="/booking")

def calculate_fare(distance_km: float) -> int:
    """Tính giá cước dựa trên khoảng cách"""
    if distance_km <= 1:
        return int(distance_km * 10000)
    elif 2 <= distance_km <= 4:
        return int(distance_km * 15000)
    else:
        return int(distance_km * 12000)


