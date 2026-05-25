from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.models import RoomInventory, Booking
from app.routes.availability import router as availability_router
from app.routes.bookings import router as booking_router
from app.routes.booking_details import router as booking_details_router

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

@app.get("/")
def root():
    return {
        "message": "Shanti Hotels Backend Running"
    }