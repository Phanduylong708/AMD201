from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.data.init import Base

class Rider(Base):
    __tablename__ = "riders"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    phone_number = Column(String(10), unique=True, nullable=False)
    is_available = Column(Boolean, default=True)
    in_riding = Column(Boolean, default=False)
    vehicle_type = Column(String(9), nullable=False)
    license_plate = Column(String(20), unique=True, nullable=False)
    driving_licence = Column(String(12), unique=True, nullable=False)
    rating = Column(Float, default=5.0)

    bookings = relationship("Booking", back_populates="rider")


class RideRequest(Base):
    __tablename__ = "ride_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    rider_id = Column(Integer, ForeignKey("riders.id"), nullable=True)  # Assigned Rider
    distance_km = Column(Float, nullable=False)  # Distance between User and Rider
    status = Column(String, default="Pending")  # "Pending", "Assigned", "Completed"

    rider = relationship("Rider")
