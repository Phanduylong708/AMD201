from fastapi import HTTPException, status

class RideMatchingError:
    USER_NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found in distance matrix")
    NO_RIDERS_AVAILABLE = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No available riders")
