from pydantic import BaseModel

class AvailabilityUpdate(BaseModel):
    is_available: bool