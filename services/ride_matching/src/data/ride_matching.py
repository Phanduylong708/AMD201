from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.data.init import Base

class Rider(Base):
    __tablename__ = "riders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(String, default="Available")  # Available, Busy
    latitude = Column(Integer, nullable=False)
    longitude = Column(Integer, nullable=False)

    bookings = relationship("Booking", back_populates="rider")