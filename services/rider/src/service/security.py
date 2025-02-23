from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
from src.error import RiderError

def authenticate_rider(username: str, password: str):
    rider = rider.get_rider_by_username(username)
    if not rider:
        raise RiderError.INVALID_CREDENTIALS  #Specific error message
    if not verify_password(password, rider.hashed_password):
        raise RiderError.INVALID_CREDENTIALS
    return rider