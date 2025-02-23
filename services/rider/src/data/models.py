from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base

Base = declarative_base()


#Retrieves a rider from the database using their username.
def get_rider_by_username(db: Session, username: str):
    return db.query(Rider).filter(Rider.username == username).first()

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
    is_available = Column(Boolean, default=True)                                #Status of rider availability
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())           
    in_riding = Column(Boolean, default=False, nullable=False)                  #Status of rider in a ride
