# Shanti Hotels API

A FastAPI-based backend service designed to manage room inventory, bookings, guest communications, support, and telephony logs for Shanti Hotels. The service provides endpoints to check room availability, manage bookings, issue support tickets, send confirmation emails, log phone calls, and handle human escalations while persisting data to a PostgreSQL database.

---

## 🚀 Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Database ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
- **Database:** PostgreSQL (with Supabase support)
- **Email Delivery:** [Resend](https://resend.com/)
- **Server:** [Uvicorn](https://www.uvicorn.org/)
- **Data Validation:** [Pydantic](https://docs.pydantic.dev/)
- **Environment Management:** `python-dotenv`

---

## 📁 Project Structure

```text
├── app/
│   ├── routes/
│   │   ├── availability.py      # Route for checking room availability
│   │   ├── bookings.py          # Route for booking rooms
│   │   ├── booking_details.py   # Route for retrieving booking details
│   │   ├── cancel_booking.py    # Route for cancelling booking and restoring inventory
│   │   ├── modify_booking.py    # Route for modifying bookings & inventory adjustments
│   │   ├── send_email.py        # Route for sending email confirmations via Resend
│   │   ├── support_ticket.py    # Route for logging and managing support tickets
│   │   ├── human_escalation.py  # Route for transferring calls to human agents
│   │   ├── call_logs.py         # Route for logging AI assistant call details
│   │   └── check_booking.py     # Empty router placeholder (unused)
│   ├── database.py              # Database configuration and connection setup
│   ├── main.py                  # Application entrypoint & FastAPI setup
│   ├── models.py                # SQLAlchemy Models (RoomInventory, Booking, SupportTicket, etc.)
│   └── schemas.py               # Pydantic validation schemas
├── .env                         # Environment variables (Database URL, API Keys)
├── .env.example                 # Example environment variables
├── .gitignore                   # Files ignored in Git
├── Procfile                     # Deployment run command
├── README.md                    # Project documentation (this file)
└── requirements.txt             # Python dependencies
```

---

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.8+
- PostgreSQL database (or Supabase instance)
- Resend API Key (for email features)

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
Create a `.env` file in the root directory (using `.env.example` as a reference) and specify your configuration:
```env
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database_name>
RESEND_API_KEY=your_resend_api_key_here
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

The application automatically creates database tables on startup if they do not exist.

### 1. `RoomInventory` (`room_inventory`)
Stores hotel room types, pricing, and available counts.
- `id` (UUID, Primary Key)
- `room_type` (String, Unique, e.g., "Deluxe", "Suite")
- `total_rooms` (Integer)
- `available_rooms` (Integer)
- `price_per_night` (Numeric)
- `updated_at` (Timestamp)

### 2. `Booking` (`bookings`)
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

### 3. `SupportTicket` (`support_tickets`)
Tracks guest issues and complaints.
- `id` (UUID, Primary Key)
- `ticket_id` (String, Unique, e.g., "SUP12345")
- `guest_name` (String)
- `phone_number` (String)
- `room_number` (String, Optional)
- `issue_category` (String)
- `issue_description` (String)
- `priority_level` (String, default "Medium")
- `status` (String, default "Open")
- `created_at` (Timestamp)

### 4. `HumanEscalation` (`human_escalations`)
Tracks requests to escalate an AI conversation to a human support agent.
- `id` (UUID, Primary Key)
- `escalation_id` (String, Unique, e.g., "ESC12345")
- `guest_name` (String)
- `phone_number` (String)
- `reason` (String)
- `conversation_summary` (String)
- `status` (String, default "Pending")
- `created_at` (Timestamp)

### 5. `CallLog` (`call_logs`)
Stores details and transcripts of AI assistant voice calls.
- `id` (UUID, Primary Key)
- `caller_number` (String)
- `intent` (String)
- `transcript` (String)
- `tool_used` (String)
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

### 4. Get Booking Details
Retrieves details of an existing booking.
- **URL:** `/get-booking-details`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "booking_id": "SH68421"
  }
  ```
- **Response (Success):**
  ```json
  {
    "success": true,
    "booking": {
      "booking_id": "SH68421",
      "guest_name": "John Doe",
      "room_type": "Deluxe",
      "check_in_date": "2026-06-01",
      "check_out_date": "2026-06-05",
      "guests": 2,
      "booking_status": "Confirmed"
    }
  }
  ```
- **Response (Failure):**
  ```json
  {
    "success": false,
    "message": "Booking not found"
  }
  ```

### 5. Cancel Booking
Cancels a booking and restores room inventory (available rooms count is incremented).
- **URL:** `/cancel-booking`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "booking_id": "SH68421",
    "phone_number": "+1234567890",
    "reason": "Change of plans"
  }
  ```
- **Response (Success):**
  ```json
  {
    "success": true,
    "message": "Booking cancelled successfully",
    "booking_id": "SH68421"
  }
  ```

### 6. Modify Booking
Modifies booking parameters (dates, guests, or room type). Adjusts inventory automatically if the room type is changed.
- **URL:** `/modify-booking`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "booking_id": "SH68421",
    "new_room_type": "Suite",
    "new_guests": 3
  }
  ```
- **Response (Success):**
  ```json
  {
    "success": true,
    "message": "Booking modified successfully",
    "booking_id": "SH68421",
    "updated_booking": {
      "room_type": "Suite",
      "check_in_date": "2026-06-01",
      "check_out_date": "2026-06-05",
      "guests": 3
    }
  }
  ```

### 7. Send Email Confirmation
Sends a transactional email confirmation to a guest using Resend.
- **URL:** `/send-email-confirmation`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "to_email": "guest@example.com",
    "subject": "Booking Confirmation - Shanti Hotels",
    "message": "Your booking for a Deluxe room from 2026-06-01 to 2026-06-05 is confirmed. Booking ID: SH68421."
  }
  ```
- **Response (Success):**
  ```json
  {
    "success": true,
    "response": {
      "id": "email_id_hash"
    }
  }
  ```

### 8. Create Support Ticket
Creates a support ticket to record guest issues (e.g. maintenance, service request).
- **URL:** `/create-support-ticket`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "guest_name": "John Doe",
    "phone_number": "+1234567890",
    "room_number": "304",
    "issue_category": "Plumbing",
    "issue_description": "Water heater in room 304 is not working.",
    "priority_level": "High"
  }
  ```
- **Response (Success):**
  ```json
  {
    "success": true,
    "ticket_id": "SUP84729",
    "message": "Support ticket created successfully"
  }
  ```

### 9. Transfer to Human
Registers an escalation request to alert human support staff.
- **URL:** `/transfer-to-human`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "guest_name": "John Doe",
    "phone_number": "+1234567890",
    "reason": "Wants to speak to a manager about a billing dispute",
    "conversation_summary": "Guest called checking booking status, then complained about an extra charge on their card."
  }
  ```
- **Response (Success):**
  ```json
  {
    "success": true,
    "escalation_id": "ESC48192",
    "message": "Human support team has been notified"
  }
  ```

### 10. Log Call
Logs conversational data from telephony integrations.
- **URL:** `/log-call`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "caller_number": "+1234567890",
    "intent": "Modify Booking",
    "transcript": "I would like to change my room type from Deluxe to a Suite.",
    "tool_used": "modify_booking"
  }
  ```
- **Response (Success):**
  ```json
  {
    "success": true,
    "message": "Call logged successfully"
  }
  ```
