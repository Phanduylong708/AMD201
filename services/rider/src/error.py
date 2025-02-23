from fastapi import HTTPException, status

class RiderError:
    RIDER_NOT_FOUND = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Rider not found"
    )

    USERNAME_EXISTS = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="This username is already taken. Please choose another one."
    )

    EMAIL_EXISTS = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="This email is already registered. Please use another email or try to login."
    )

    PHONE_EXISTS = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="This phone number is already registered. Please use another number or try to login."
    )

    VEHICLE_EXISTS = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="This vehicle is already registered with another rider."
    )

    INVALID_CREDENTIALS = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password."
    )

    PERMISSION_DENIED = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You don't have permission to perform this action."
    )

    DATABASE_ERROR = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="A database error occurred. Please try again later."
    )

    UNEXPECTED_ERROR = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An unexpected error occurred. Please try again later."
    )

    DUPLICATE_ENTRY = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Duplicate entry found. Please check your username, email, phone number, or license plate."
    )
