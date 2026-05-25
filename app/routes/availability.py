from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import RoomInventory
from app.schemas import AvailabilityRequest

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/check-availability")
def check_availability(
    data: AvailabilityRequest,
    db: Session = Depends(get_db)
):

    room = db.query(RoomInventory).filter(
        RoomInventory.room_type == data.room_type
    ).first()

    if room and room.available_rooms > 0:

        return {
            "available": True,
            "room_type": room.room_type,
            "price_per_night": float(room.price_per_night),
            "rooms_left": room.available_rooms
        }

    return {
        "available": False
    }