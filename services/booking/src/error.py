<<<<<<< HEAD
from fastapi import HTTPException, status

class BookingError:
    BOOKING_NOT_FOUND = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Booking not found"
    )
    
    RIDER_NOT_AVAILABLE = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="No available riders at the moment. Please try again later."
    )
    
    INVALID_BOOKING_STATUS = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid booking status update request."
    )
    
    PAYMENT_FAILED = HTTPException(
        status_code=status.HTTP_402_PAYMENT_REQUIRED,
        detail="Payment processing failed. Please try again."
    )
    
    UNAUTHORIZED_ACCESS = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized access to this booking."
    )
=======
class Missing(Exception):
    def __init__(self, msg:str):
        self.msg = msg

class Duplicate(Exception):
    def __init__(self, msg:str):
        self.msg = msg
>>>>>>> 1be5fee6da39d2c0918f60eb2ec9363da84caba5
