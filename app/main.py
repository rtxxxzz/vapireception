from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import engine, Base
from typing import Dict
from app.routes.availability import router as availability_router
from app.routes.bookings import router as booking_router
from app.routes.booking_details import router as booking_details_router
from app.routes.cancel_booking import router as cancel_booking_router
from app.routes.modify_booking import router as modify_booking_router
from app.routes.send_email import router as send_email_router
from app.routes.support_ticket import router as support_ticket_router
from app.routes.human_escalation import router as human_escalation_router
from app.routes.call_logs import router as call_logs_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables if they do not exist
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Shanti Hotels API",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(availability_router)

app.include_router(booking_router)

app.include_router(booking_details_router)

app.include_router(cancel_booking_router)

app.include_router(modify_booking_router)

app.include_router(send_email_router)

app.include_router(support_ticket_router)

app.include_router(human_escalation_router)

app.include_router(call_logs_router)

@app.get("/")
def root():
    return {
        "message": "Shanti Hotels Backend Running"
    }