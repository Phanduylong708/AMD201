from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.sql import func
from src.data.init import Base

class Rider(Base):
    __tablename__ = "riders"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone_number = Column(String(10), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    vehicle_type = Column(String(9), nullable=False)
    license_plate = Column(String(20), unique=True, nullable=False)
    driving_licence = Column(String(12), unique=True, nullable=False)
    rating = Column(Float, default=5.0)
    is_available = Column(Boolean, default=True)
    in_riding = Column(Boolean, default=False, nullable=False)
