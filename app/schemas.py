from typing import Optional
from pydantic import BaseModel
from datetime import date

class AvailabilityRequest(BaseModel):
    room_type: str
    check_in_date: date
    check_out_date: date
    guests: int


class BookingRequest(BaseModel):
    guest_name: str
    phone_number: str
    room_type: str
    check_in_date: date
    check_out_date: date
    guests: int

class BookingLookupRequest(BaseModel):
    booking_id: str
    phone_number: Optional[str] = None

class CancelBookingRequest(BaseModel):
    booking_id: str
    phone_number: str
    reason: Optional[str] = None