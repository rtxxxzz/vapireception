from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import CallLog
from app.schemas import CallLogRequest

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/log-call")
def log_call(
    data: CallLogRequest,
    db: Session = Depends(get_db)
):

    log = CallLog(
        caller_number=data.caller_number,
        intent=data.intent,
        transcript=data.transcript,
        tool_used=data.tool_used
    )

    db.add(log)

    db.commit()

    return {
        "success": True,
        "message": "Call logged successfully"
    }