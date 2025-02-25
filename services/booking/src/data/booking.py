from sqlalchemy.orm import Session
from src.data.models import Booking
from src.model import booking as schemas
from src.data.init import get_db
from AMD201.services.booking.src.error import BookingError
from src.service.rider import get_available_riders

def create_booking(booking: schemas.BookingCreate):
    db: Session = next(get_db())
    db_booking = Booking(
        user_id=booking.user_id,
        rider_id=booking.rider_id,
        status=booking.status,
        distance_km=booking.distance_km,
        fare=booking.fare
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def get_booking(booking_id: int):
    db = next(get_db())
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise BookingError.BOOKING_NOT_FOUND
    return booking

def update_booking_status(booking_id: int, status: str):
    db = next(get_db())
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise BookingError.BOOKING_NOT_FOUND
    booking.status = status
    db.commit()
    db.refresh(booking)
    return booking

def find_nearest_rider(pickup_location):
    riders = get_available_riders()  # Lấy danh sách tài xế sẵn có
    if not riders:
        return None
    # Giả sử rider có tọa độ (lat, lon), ta tính khoảng cách đơn giản
    riders.sort(key=lambda r: distance_between(pickup_location, (r.lat, r.lon)))
    return riders[0]  # Trả về tài xế gần nhất

#cập nhập trạng thái chuyến ddi
def update_booking_status(booking_id: int, status: str):
    booking = get_booking(booking_id)
    if not booking:
        raise BookingError.NOT_FOUND
    if status not in ["Pending", "In Progress", "Completed", "Canceled"]:
        raise BookingError.INVALID_STATUS
    booking.status = status
    save_booking(booking)
    return booking