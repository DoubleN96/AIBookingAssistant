# main.py
from fastapi import FastAPI, Request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os

app = FastAPI()

# Set up Twilio client with your Twilio Account SID and Auth Token
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

# Your Twilio phone number
twilio_phone_number = os.environ['TWILIO_PHONE_NUMBER']

@app.post("/incoming")
async def handle_incoming_message(request: Request):
    form = await request.form()
    message = form.get("Body")
    sender = form.get("From")

    # Do something with the message (e.g., store it in a database, process it, etc.)

    # Reply with a simple text message
    resp = MessagingResponse()
    resp.message("Thank you for your message!")

    return {"twiml": str(resp)}

@app.get("/send")
async def send_message(to: str, body: str):
    message = client.messages.create(
        body=body,
        from_=f"whatsapp:{twilio_phone_number}",
        to=f"whatsapp:{to}",
    )

    return {"status": "sent", "sid": message.sid}
