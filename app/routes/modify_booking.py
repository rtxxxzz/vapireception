from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Booking, RoomInventory
from app.schemas import ModifyBookingRequest

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/modify-booking")
def modify_booking(
    data: ModifyBookingRequest,
    db: Session = Depends(get_db)
):

    # FIND BOOKING
    booking = db.query(Booking).filter(
        Booking.booking_id == data.booking_id
    ).first()

    if not booking:
        return {
            "success": False,
            "message": "Booking not found"
        }

    # CANNOT MODIFY CANCELLED BOOKINGS
    if booking.booking_status == "Cancelled":
        return {
            "success": False,
            "message": "Cancelled bookings cannot be modified"
        }

    # ROOM CHANGE LOGIC
    if data.new_room_type:

        # FIND NEW ROOM
        new_room = db.query(RoomInventory).filter(
            RoomInventory.room_type == data.new_room_type
        ).first()

        if not new_room:
            return {
                "success": False,
                "message": "Requested room type does not exist"
            }

        # CHECK AVAILABILITY
        if new_room.available_rooms <= 0:
            return {
                "success": False,
                "message": "Requested room type unavailable"
            }

        # RESTORE OLD ROOM INVENTORY
        old_room = db.query(RoomInventory).filter(
            RoomInventory.room_type == booking.room_type
        ).first()

        if old_room:
            old_room.available_rooms += 1

        # REDUCE NEW ROOM INVENTORY
        new_room.available_rooms -= 1

        # UPDATE BOOKING ROOM
        booking.room_type = data.new_room_type

    # DATE MODIFICATIONS
    if data.new_check_in_date:
        booking.check_in_date = data.new_check_in_date

    if data.new_check_out_date:
        booking.check_out_date = data.new_check_out_date

    # GUEST COUNT
    if data.new_guests:
        booking.guests = data.new_guests

    db.commit()

    return {
        "success": True,
        "message": "Booking modified successfully",
        "booking_id": booking.booking_id,
        "updated_booking": {
            "room_type": booking.room_type,
            "check_in_date": str(booking.check_in_date),
            "check_out_date": str(booking.check_out_date),
            "guests": booking.guests
        }
    }