from sqlalchemy.orm import Session
from src.data.models import Rider


def get_rider_by_username(db: Session, username: str):
    """
    Retrieves a rider from the database using their username.
    """
    print(f"🔍 Searching for rider: {username}")  # Debugging line

    rider = db.query(Rider).filter(Rider.username == username).first()
    
    if not rider:
        print("❌ Rider not found in the database")  # Debugging line
    else:
        print(f"✅ Rider found: {rider.username}")  # Debugging line
    
    return rider

