from sqlalchemy.orm import Session
from src.data.models import Rider
from src.model import rider as schemas
from src.data.init import get_db
from src.service.security import get_password_hash  # Import hashing function

def create_rider(rider: schemas.RiderCreate):
    db: Session = next(get_db())
    hashed_password = get_password_hash(rider.password)  # Actual hashing
    db_rider = Rider(
        username=rider.username,
        email=rider.email,
        phone_number=rider.phone_number,
        full_name=rider.full_name,
        vehicle_type=rider.vehicle_type,
        license_plate=rider.license_plate,
        rating=rider.rating,
        is_available=rider.is_available,
        hashed_password=hashed_password  # Use hashed password
    )
    db.add(db_rider)
    db.commit()
    db.refresh(db_rider)
    return db_rider
