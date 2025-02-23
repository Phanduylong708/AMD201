from sqlalchemy.orm import Session
from src.data.models import Rider
from src.model import rider as schemas
from src.data.init import get_db
from src.service.security import get_password_hash
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.error import RiderError, HTTPException
from fastapi import Depends




def create_rider(rider: schemas.RiderCreate, db: Session = Depends(get_db)):
    try:
        db_rider = Rider(
            username=rider.username,
            email=rider.email,
            phone_number=rider.phone_number,  
            full_name=rider.full_name,
            vehicle_type=rider.vehicle_type,
            license_plate=rider.license_plate,
            driving_licence=rider.driving_licence,
            rating=5.0,             
            is_available=True,     
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

def update_rider(rider_id: int, rider: schemas.RiderUpdate, current_user: dict, db: Session = Depends(get_db)):
#Updates rider profile while ensuring only the logged-in rider can update their own data.
    db_rider = db.query(Rider).filter(Rider.id == rider_id).first()
    if not db_rider:
        raise HTTPException(status_code=404, detail="Rider not found")


    #Ensure riders can only update their own profile
    if current_user["sub"] != db_rider.username:
        raise HTTPException(status_code=403, detail="Not authorized to update this profile.")


    #Prevent changes to `rating` & `is_available`
    update_data = rider.dict(exclude_unset=True)
    if "rating" in update_data:
        del update_data["rating"]
    if "is_available" in update_data:
        del update_data["is_available"]

    for key, value in update_data.items():
        setattr(db_rider, key, value)

    try:
        db.commit()
        db.refresh(db_rider)
        return db_rider
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Update failed due to duplicate entry.")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
