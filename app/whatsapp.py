import json
from fastapi import FastAPI, Request, Response, status, File, UploadFile, Form
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests

import whatsapp as wa

creds = {
    "username": "your_username",
    "password": "your_password",
    "business_number": "your_business_number"
}
url = "https://api.chat-api.com/instance12345/sendMessage?token=your_token"


def handle_message(data):
    # extract message data
    message = data['messages'][0]['message']
    chat_id = data['messages'][0]['chatId']
    phone_number = data['messages'][0]['profile']['phoneNumber']
    
    # handle message based on its content
    if message.startswith("Hi"):
        response_message = "Hello, I am your digital booking assisttant. How can I assist you today?"
    else:
        response_message = "Sorry, I didn't understand your message."

    # send response message using WhatsApp Business API
    send_message(chat_id, response_message)
    
    return {"status": "success"}
