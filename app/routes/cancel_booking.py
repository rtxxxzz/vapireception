from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Booking, RoomInventory
from app.schemas import CancelBookingRequest

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/cancel-booking")
def cancel_booking(
    data: CancelBookingRequest,
    db: Session = Depends(get_db)
):

    # FIND BOOKING
    booking = db.query(Booking).filter(
        Booking.booking_id == data.booking_id
    ).first()

    # BOOKING NOT FOUND
    if not booking:
        return {
            "success": False,
            "message": "Booking not found"
        }

    # ALREADY CANCELLED
    if booking.booking_status == "Cancelled":
        return {
            "success": False,
            "message": "Booking already cancelled"
        }

    # FIND ROOM INVENTORY
    room = db.query(RoomInventory).filter(
        RoomInventory.room_type == booking.room_type
    ).first()

    # RESTORE INVENTORY
    if room:
        room.available_rooms += 1

    # UPDATE BOOKING STATUS
    booking.booking_status = "Cancelled"

    db.commit()

    return {
        "success": True,
        "message": "Booking cancelled successfully",
        "booking_id": booking.booking_id
    }