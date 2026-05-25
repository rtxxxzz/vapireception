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


class ModifyBookingRequest(BaseModel):
    booking_id: str

    new_room_type: Optional[str] = None

    new_check_in_date: Optional[date] = None

    new_check_out_date: Optional[date] = None

    new_guests: Optional[int] = None

class SendEmailRequest(BaseModel):
    to_email: str
    subject: str
    message: str

class SupportTicketRequest(BaseModel):
    guest_name: str
    phone_number: str
    room_number: str
    issue_category: str
    issue_description: str
    priority_level: str = "Medium"

class HumanEscalationRequest(BaseModel):
    guest_name: str
    phone_number: str
    reason: str
    conversation_summary: str

class CallLogRequest(BaseModel):
    caller_number: str
    intent: str
    transcript: str
    tool_used: str