import requests
import json
from whatsapp import WhatsAppAPI, message, client


# Define the FastAPI route URL
fastapi_url = "http://chatbot_fastapi:5300/audio"

# When you receive an audio message, extract the sender and audio data
sender = message.get_sender()
audio_data = message.get_audio_data()

# Make a POST request to the FastAPI route with the audio data as the request body
response = requests.post(fastapi_url, json={"sender": sender, "audio": audio_data})

# Extract the text response from the JSON response
audio_text = response.json()["text"]

# Send the text response back to the sender as a WhatsApp message
client.send_message(sender, audio_text)
