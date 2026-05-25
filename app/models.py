from sqlalchemy import Column, String, Integer, Numeric, Date, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class RoomInventory(Base):
    __tablename__ = "room_inventory"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    room_type = Column(String, unique=True, nullable=False)

    total_rooms = Column(Integer, nullable=False)

    available_rooms = Column(Integer, nullable=False)

    price_per_night = Column(Numeric, nullable=False)

    updated_at = Column(TIMESTAMP, server_default=func.now())


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    booking_id = Column(String, unique=True, nullable=False)

    guest_name = Column(String, nullable=False)

    phone_number = Column(String, nullable=False)

    room_type = Column(String, nullable=False)

    guests = Column(Integer, nullable=False)

    check_in_date = Column(Date, nullable=False)

    check_out_date = Column(Date, nullable=False)

    booking_status = Column(String, default="Confirmed")

    created_at = Column(TIMESTAMP, server_default=func.now())


class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    ticket_id = Column(String, unique=True, nullable=False)

    guest_name = Column(String, nullable=False)

    phone_number = Column(String, nullable=False)

    room_number = Column(String)

    issue_category = Column(String, nullable=False)

    issue_description = Column(String, nullable=False)

    priority_level = Column(String, default="Medium")

    status = Column(String, default="Open")

    created_at = Column(TIMESTAMP, server_default=func.now())

class HumanEscalation(Base):
    __tablename__ = "human_escalations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    escalation_id = Column(String, unique=True, nullable=False)

    guest_name = Column(String)

    phone_number = Column(String)

    reason = Column(String, nullable=False)

    conversation_summary = Column(String)

    status = Column(String, default="Pending")

    created_at = Column(TIMESTAMP, server_default=func.now())

class CallLog(Base):
    __tablename__ = "call_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    caller_number = Column(String)

    intent = Column(String)

    transcript = Column(String)

    tool_used = Column(String)

    created_at = Column(TIMESTAMP, server_default=func.now())