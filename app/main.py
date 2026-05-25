from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.models import RoomInventory, Booking
from app.routes.availability import router as availability_router
from app.routes.bookings import router as booking_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables if they do not exist
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Shanti Hotels API",
    lifespan=lifespan
)

app.include_router(availability_router)

app.include_router(booking_router)

@app.get("/")
def root():
    return {
        "message": "Shanti Hotels Backend Running"
    }