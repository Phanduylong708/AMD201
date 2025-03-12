from sqlalchemy.orm import Session
from src.data.models import Rider
from src.model import rider as schemas
from src.service.security import get_password_hash
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.error import HTTPException
from src.error import RiderError


def get_rider(db: Session, rider_id: int):
    return db.query(Rider).filter(Rider.id == rider_id).first()


def get_riders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Rider).offset(skip).limit(limit).all()


def create_rider(rider: schemas.RiderCreate, db: Session):
    try:
        db_rider = Rider(
            username=rider.username,
            email=rider.email,
            phone_number=rider.phone_number,
            full_name=rider.full_name,
            vehicle_type=rider.vehicle_type,
            license_plate=rider.license_plate,
            driving_licence=rider.driving_licence,
            hashed_password=get_password_hash(rider.password),
            rating=5.0,             
            is_available=True     
        )
        db.add(db_rider)
        db.commit()
        db.refresh(db_rider)
        return db_rider
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig) if hasattr(e, 'orig') and e.orig else str(e)
        raise RiderError.parse_duplicate_error(error_message)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def update_rider(rider_id: int, rider: schemas.RiderUpdate, current_user: dict, db: Session):  # ✅ Fix
    db_rider = db.query(Rider).filter(Rider.id == rider_id).first()
    if not db_rider:
        raise HTTPException(status_code=404, detail="Rider not found")

    # Ensure riders can only update their own profile
    if current_user["sub"] != db_rider.username:
        raise HTTPException(status_code=403, detail="Not authorized to update this profile.")

    # Prevent changes to `rating` & `is_available`
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
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig) if hasattr(e, 'orig') and e.orig else str(e)
        raise RiderError.parse_duplicate_error(error_message)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def delete_rider(db: Session, rider_id: int):
    """
    Deletes a rider from the database.
    Returns True if deleted, False if the rider does not exist.
    """
    db_rider = db.query(Rider).filter(Rider.id == rider_id).first()
    if not db_rider:
        return False  # Rider not found

    db.delete(db_rider)
    db.commit()
    return True  # Successfully deleted



def update_availability(db: Session, rider_id: int, is_available: bool):
    """
    Updates only the availability status of a rider.
    Returns the updated rider object if successful, or None if the rider does not exist.
    """
    db_rider = db.query(Rider).filter(Rider.id == rider_id).first()
    if not db_rider:
        return None  # Rider not found

    db_rider.is_available = is_available  # ✅ Update only availability
    db.commit()
    db.refresh(db_rider)  # ✅ Refresh to get updated values
    return db_rider  # ✅ Return updated rider

