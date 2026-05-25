from fastapi import APIRouter
from dotenv import load_dotenv
import resend
import os

from app.schemas import SendEmailRequest

load_dotenv()

router = APIRouter()

resend.api_key = os.getenv("RESEND_API_KEY")

@router.post("/send-email-confirmation")
def send_email_confirmation(data: SendEmailRequest):

    try:

        response = resend.Emails.send({
            "from": "Shanti Hotels <onboarding@resend.dev>",
            "to": [data.to_email],
            "subject": data.subject,
            "html": f"""
                <h2>Shanti Hotels</h2>
                <p>{data.message}</p>
            """
        })

        return {
            "success": True,
            "response": response
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }