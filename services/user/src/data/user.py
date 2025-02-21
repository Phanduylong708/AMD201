from src.data import models
from src.data.init import get_db
from src.model import user as schemas
from src.service.security import get_password_hash, verify_password
from src.error import UserError
import re

def get_user(user_id):
    db = next(get_db())
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(email):
    db = next(get_db())
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(username):
    db = next(get_db())
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        print(f"get_user_by_username: Found user '{user.username}' with hashed_password '{user.hashed_password}'")
    else:
        print(f"get_user_by_username: No user found for username '{username}'")
    return user

def get_users(skip=0, limit=100):
    db = next(get_db())
    return db.query(models.User).offset(skip).limit(limit).all()

def validate_password(password):
    """
    Validate that password meets requirements:
    - At least 8 characters long
    - Contains at least one letter and one number
    """
    if len(password) < 8:
        return False
    if not re.search(r"[A-Za-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    return True

def create_user(user: schemas.UserCreate):
    db = next(get_db())

    if not validate_password(user.password):
        raise UserError.INVALID_PASSWORD

    if db.query(models.User).filter(models.User.username == user.username).first():
        raise UserError.USERNAME_EXISTS

    if db.query(models.User).filter(models.User.email == user.email).first():
        raise UserError.EMAIL_EXISTS

    if db.query(models.User).filter(models.User.phone_number == user.phone_number).first():
        raise UserError.PHONE_EXISTS

    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(user_id, user: schemas.UserUpdate):
    db = next(get_db())
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise UserError.USER_NOT_FOUND
    
    update_data = user.model_dump(exclude_unset=True)
    
    if 'username' in update_data:
        existing = db.query(models.User).filter(models.User.username == update_data['username']).first()
        if existing and existing.id != user_id:
            raise UserError.USERNAME_EXISTS
            
    if 'email' in update_data:
        existing = db.query(models.User).filter(models.User.email == update_data['email']).first()
        if existing and existing.id != user_id:
            raise UserError.EMAIL_EXISTS
            
    if 'phone_number' in update_data:
        existing = db.query(models.User).filter(models.User.phone_number == update_data['phone_number']).first()
        if existing and existing.id != user_id:
            raise UserError.PHONE_EXISTS
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(user_id):
    db = next(get_db())
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise UserError.USER_NOT_FOUND
    
    db.delete(db_user)
    db.commit()
    return True

def authenticate_user(username, password):
    user = get_user_by_username(username)
    if not user:
        print("authenticate_user: User not found for username:", username)
        raise UserError.INVALID_CREDENTIALS
    print(f"authenticate_user: verifying password '{password}' against hashed '{user.hashed_password}'")
    if not verify_password(password, user.hashed_password):
        print("authenticate_user: Password verification failed")
        raise UserError.INVALID_CREDENTIALS
    return user
