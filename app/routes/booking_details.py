from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Booking
from app.schemas import BookingLookupRequest

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/get-booking-details")
def get_booking_details(
    data: BookingLookupRequest,
    db: Session = Depends(get_db)
):

    booking = db.query(Booking).filter(
        Booking.booking_id == data.booking_id
    ).first()

    if not booking:
        return {
            "success": False,
            "message": "Booking not found"
        }

    return {
        "success": True,
        "booking": {
            "booking_id": booking.booking_id,
            "guest_name": booking.guest_name,
            "room_type": booking.room_type,
            "check_in_date": str(booking.check_in_date),
            "check_out_date": str(booking.check_out_date),
            "guests": booking.guests,
            "booking_status": booking.booking_status
        }
    }