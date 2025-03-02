from sqlalchemy.orm import Session
from src.data.models import User
from fastapi import HTTPException

def get_user_by_id(db: Session, user_id: int):
    """Retrieve a user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def is_user_available(db: Session, user_id: int):
    """Check if a user exists (for booking validation)."""
    return db.query(User).filter(User.id == user_id).first() is not None
