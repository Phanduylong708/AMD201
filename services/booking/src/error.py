from fastapi import HTTPException, status

class BookingError:
    @staticmethod
    def booking_not_found(detail: str = "Booking not found") -> HTTPException:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    
    @staticmethod
    def active_booking_exists(detail: str = "Active booking already exists.") -> HTTPException:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    
    @staticmethod
    def rider_not_available(detail: str = "No available riders at the moment. Please try again later.") -> HTTPException:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    
    @staticmethod
    def invalid_booking_status(detail: str = "Invalid booking status update request.") -> HTTPException:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    
    @staticmethod
    def payment_failed(detail: str = "Payment processing failed. Please try again.") -> HTTPException:
        return HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=detail)
    
    @staticmethod
    def unauthorized_access(detail: str = "Unauthorized access to this booking.") -> HTTPException:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

    @staticmethod
    def user_service_error(detail: str = "Failed to communicate with User Service.") -> HTTPException:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

    @staticmethod
    def ride_matching_service_error(detail: str = "Failed to communicate with Ride Matching Service.") -> HTTPException:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

    @staticmethod
    def rider_service_error(detail: str = "Failed to communicate with Rider Service.") -> HTTPException:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

