from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import random

from app.database import SessionLocal
from app.models import Booking, RoomInventory
from app.schemas import BookingRequest

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/book-room")
def book_room(
    data: BookingRequest,
    db: Session = Depends(get_db)
):

    room = db.query(RoomInventory).filter(
        RoomInventory.room_type == data.room_type
    ).first()

    if not room or room.available_rooms <= 0:
        return {
            "success": False,
            "message": "Room unavailable"
        }

    booking_id = f"SH{random.randint(10000,99999)}"

    booking = Booking(
        booking_id=booking_id,
        guest_name=data.guest_name,
        phone_number=data.phone_number,
        room_type=data.room_type,
        guests=data.guests,
        check_in_date=data.check_in_date,
        check_out_date=data.check_out_date
    )

    room.available_rooms -= 1

    db.add(booking)

    db.commit()

    return {
        "success": True,
        "booking_id": booking_id,
        "message": "Room booked successfully"
    }