# Shanti Hotels API

A FastAPI-based backend service designed to manage room inventory and bookings for Shanti Hotels. The service provides endpoints to check room availability and book rooms while persisting data to a database.

---

## 🚀 Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Database ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
- **Database:** PostgreSQL (with Supabase/psycopg2 support)
- **Server:** [Uvicorn](https://www.uvicorn.org/)
- **Data Validation:** [Pydantic](https://docs.pydantic.dev/)
- **Environment Management:** `python-dotenv`

---

## 📁 Project Structure

```text
├── app/
│   ├── routes/
│   │   ├── availability.py    # Route for checking room availability
│   │   ├── bookings.py        # Route for booking rooms
│   │   └── check_booking.py   # Empty router placeholder
│   ├── database.py            # Database configuration and connection setup
│   ├── main.py                # Application entrypoint & FastAPI setup
│   ├── models.py              # SQLAlchemy Models (RoomInventory, Booking)
│   └── schemas.py             # Pydantic validation schemas
├── .env                       # Environment variables (Database URL, etc.)
├── .gitignore                 # Files ignored in Git
├── Procfile                   # Deployment run command (e.g., Heroku)
├── README.md                  # Project documentation (this file)
└── requirements.txt           # Python dependencies
```

---

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.8+
- PostgreSQL database (or Supabase instance)

### 1. Clone & Navigate to the Project
```bash
git clone <repository-url>
cd vapireception
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and specify your `DATABASE_URL`:
```env
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database_name>
```

### 5. Running the Application
To run the server locally in development mode:
```bash
uvicorn app.main:app --reload
```

Alternatively, to run it as configured in the `Procfile`:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Once running, the interactive API documentation will be available at `http://127.0.0.1:8000/docs` (Swagger UI).

---

## 🗄️ Database Models

The application is configured to automatically create the database tables on startup if they do not exist:

### `RoomInventory` (`room_inventory`)
Stores hotel room types, pricing, and available counts.
- `id` (UUID, Primary Key)
- `room_type` (String, Unique, e.g., "Deluxe", "Suite")
- `total_rooms` (Integer)
- `available_rooms` (Integer)
- `price_per_night` (Numeric)
- `updated_at` (Timestamp)

### `Booking` (`bookings`)
Stores room bookings made by guests.
- `id` (UUID, Primary Key)
- `booking_id` (String, Unique, e.g., "SH12345")
- `guest_name` (String)
- `phone_number` (String)
- `room_type` (String)
- `guests` (Integer)
- `check_in_date` (Date)
- `check_out_date` (Date)
- `booking_status` (String, default "Confirmed")
- `created_at` (Timestamp)

---

## 🔌 API Endpoints

### 1. Welcome Endpoint
- **URL:** `/`
- **Method:** `GET`
- **Response:**
  ```json
  {
    "message": "Shanti Hotels Backend Running"
  }
  ```

### 2. Check Availability
Checks if rooms are available for a given room type.
- **URL:** `/check-availability`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "room_type": "Deluxe",
    "check_in_date": "2026-06-01",
    "check_out_date": "2026-06-05",
    "guests": 2
  }
  ```
- **Response (Available):**
  ```json
  {
    "available": true,
    "room_type": "Deluxe",
    "price_per_night": 150.0,
    "rooms_left": 5
  }
  ```
- **Response (Unavailable):**
  ```json
  {
    "available": false
  }
  ```

### 3. Book a Room
Creates a booking and decrements the available rooms count in the inventory.
- **URL:** `/book-room`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "guest_name": "John Doe",
    "phone_number": "+1234567890",
    "room_type": "Deluxe",
    "check_in_date": "2026-06-01",
    "check_out_date": "2026-06-05",
    "guests": 2
  }
  ```
- **Response (Success):**
  ```json
  {
    "success": true,
    "booking_id": "SH68421",
    "message": "Room booked successfully"
  }
  ```
- **Response (Failure):**
  ```json
  {
    "success": false,
    "message": "Room unavailable"
  }
  ```
