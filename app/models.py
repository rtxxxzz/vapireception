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