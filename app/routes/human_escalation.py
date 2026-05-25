from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import random

from app.database import SessionLocal
from app.models import HumanEscalation
from app.schemas import HumanEscalationRequest

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/transfer-to-human")
def transfer_to_human(
    data: HumanEscalationRequest,
    db: Session = Depends(get_db)
):

    escalation_id = f"ESC{random.randint(10000,99999)}"

    escalation = HumanEscalation(
        escalation_id=escalation_id,
        guest_name=data.guest_name,
        phone_number=data.phone_number,
        reason=data.reason,
        conversation_summary=data.conversation_summary
    )

    db.add(escalation)

    db.commit()

    return {
        "success": True,
        "escalation_id": escalation_id,
        "message": "Human support team has been notified"
    }