from src.data import user as data_user
from src.model import user as schemas
from src.error import UserError


def create_user(user: schemas.UserCreate):
    return data_user.create_user(user)


def get_user(user_id: int):
    return data_user.get_user(user_id)


def get_user_by_username(username: str):
    return data_user.get_user_by_username(username)


def get_users(skip: int = 0, limit: int = 100):
    return data_user.get_users(skip, limit)


def update_user(user_id: int, user: schemas.UserUpdate):
    return data_user.update_user(user_id, user)


def delete_user(user_id: int):
    return data_user.delete_user(user_id)


def authenticate_user(username: str, password: str):
    return data_user.authenticate_user(username, password) 