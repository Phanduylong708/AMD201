from sqlalchemy.orm import Session
from src.data.models import Rider
from src.model import rider as schemas
from src.data.init import get_db
from src.service.security import get_password_hash
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.error import RiderError, HTTPException


def create_rider(rider: schemas.RiderCreate):
    try:
        db: Session = next(get_db())

        db_rider = Rider(
            username=rider.username,
            email=rider.email,
            phone_number=rider.phone_number,  # ✅ Added phone number
            full_name=rider.full_name,
            vehicle_type=rider.vehicle_type,
            license_plate=rider.license_plate,
            driving_licence=rider.driving_licence,
            rating=5.0,  #Default rating (riders cannot set their own rating)
            is_available=True,  #Default availability (riders cannot set it)
            hashed_password=get_password_hash(rider.password),  #Hash the password
        )
        db.add(db_rider)
        db.commit()
        db.refresh(db_rider)
        return db_rider
    except IntegrityError as e:
        db.rollback()
        if "username" in str(e):
            raise RiderError.USERNAME_EXISTS
        elif "email" in str(e):
            raise RiderError.EMAIL_EXISTS
        elif "phone_number" in str(e):
            raise RiderError.PHONE_EXISTS
        elif "license_plate" in str(e):
            raise RiderError.VEHICLE_EXISTS
        elif "driving_licence" in str(e):
            raise HTTPException(status_code=400, detail="This driving licence is already registered.")
        raise RiderError.DATABASE_ERROR
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def update_rider(rider_id: int, rider: schemas.RiderUpdate):
    db: Session = next(get_db())
    db_rider = db.query(Rider).filter(Rider.id == rider_id).first()
    if not db_rider:
        return None
    for key, value in rider.dict(exclude_unset=True).items():
        setattr(db_rider, key, value)
    db.commit()
    db.refresh(db_rider)
    return db_rider
