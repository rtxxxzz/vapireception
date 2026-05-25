from fastapi import FastAPI

from app.routes.availability import router as availability_router
from app.routes.bookings import router as booking_router

app = FastAPI(
    title="Shanti Hotels API"
)

app.include_router(availability_router)

app.include_router(booking_router)

@app.get("/")
def root():
    return {
        "message": "Shanti Hotels Backend Running"
    }