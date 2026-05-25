from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import random

from app.database import SessionLocal
from app.models import SupportTicket
from app.schemas import SupportTicketRequest

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create-support-ticket")
def create_support_ticket(
    data: SupportTicketRequest,
    db: Session = Depends(get_db)
):

    ticket_id = f"SUP{random.randint(10000,99999)}"

    ticket = SupportTicket(
        ticket_id=ticket_id,
        guest_name=data.guest_name,
        phone_number=data.phone_number,
        room_number=data.room_number,
        issue_category=data.issue_category,
        issue_description=data.issue_description,
        priority_level=data.priority_level
    )

    db.add(ticket)

    db.commit()

    return {
        "success": True,
        "ticket_id": ticket_id,
        "message": "Support ticket created successfully"
    }