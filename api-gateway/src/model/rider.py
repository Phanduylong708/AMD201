from sqlalchemy import Column, Integer, String
from src.data.init import Base

class Rider(Base):
    __tablename__ = "rider"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(int(10), index=True)
    email = Column(String, index=True)
    rating = Column(Integer, index=True)
    vehicle_type = Column(String, index=True)
    vehicle_plate = Column(String, index=True)
    Driver_registration = Column(String, index=True)