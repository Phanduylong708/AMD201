from sqlalchemy import Column, Integer, String, Float
from src.data.init import Base

class Rider(Base):
    __tablename__ = "riders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    status = Column(String, default="Available")  # Available or Busy
    vehicle_type = Column(String, nullable=False)
    license_plate = Column(String, unique=True, nullable=False)
    rating = Column(Float, default=5.0)  # Default rating is 5 stars
