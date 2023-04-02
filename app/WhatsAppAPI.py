from fastapi import FastAPI, HTTPException
from whatsapp_business_api import WhatsAppBusinessAPI

app = FastAPI()

class WhatsAppAPIError(Exception):
    pass

class WhatsAppBusinessAPIWrapper:
    def __init__(self, whisper_integration=True):
        self.api = WhatsAppBusinessAPI(whisper_integration=whisper_integration)

    def get_messages(self):
        try:
            return self.api.get_messages()
        except Exception as e:
            raise WhatsAppAPIError(str(e))

wa_api_wrapper = WhatsAppBusinessAPIWrapper()

@app.get("/whatsapp-business-api")
def get_whatsapp_business_api():
    try:
        messages = wa_api_wrapper.get_messages()
        return messages
    except WhatsAppAPIError as e:
        raise HTTPException(status_code=500, detail=str(e))
