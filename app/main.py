import os
import re
import logging
import openai

from ast import literal_eval

from fastapi import FastAPI, HTTPException, Request, status, Form
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from twilio.twiml.messaging_response import MessagingResponse
from typing import Tuple
import requests
# import speech_recognition as sr

from pydantic import BaseModel

from time import perf_counter

from decouple import config


from app.conversation_manager.context_memory import (
    get_response, get_booking_chain, openai_chat_completion_ner_response
)
from app.conversation_manager.conversation_contexts import (
    recommend_booking, ask_for_booking_details, get_location_recommendations_response,
    ask_about_general_requirements_response
)
from app.pydantic_models import TextItem, BookingItem

from app.data.data_loaders import get_room_dataframe
from app.vectorizers.sentence_transformer import get_data_vectors
from app.redis_manager.redis_connector import get_redis_connector, create_flat_index, load_vectors


APP_VERSION = os.environ.get('APP_VERSION', None)

app = FastAPI(
    root_path=os.environ.get('FAST_API_ROOT_PATH', ''),
    title="REST API for interacting with chatGPT model.",
    version=APP_VERSION
)

# openai.api_key = config("OPENAI_API_KEY")
whatsapp_number = config("TO_NUMBER")


logging.info('☺ ☺ ☺ waiting for input ☺ ☺ ☺')

BOOKINGS_CACHE = {}
BOOKING_REQUEST = {}
app.booking_demo_history = []
app.interaction_count = 0

DATA, CITY_MAPPING = get_room_dataframe()

DATA_VECTORS = get_data_vectors(DATA)
REDIS_CONNECTOR = get_redis_connector('redis')

REDIS_CONNECTOR.flushall()

create_flat_index(
    REDIS_CONNECTOR,
    'item_keyword_vector',
    DATA.shape[0],
    768,
    'COSINE'
)
load_vectors(
    REDIS_CONNECTOR, DATA.to_dict(orient='index'), DATA_VECTORS, 'item_keyword_vector'
)

BOOKING_CHAIN = get_booking_chain()


def register_exception(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
        # or logger.error(f'{exc}')
        logging.error(request, exc_str)
        content = {'status_code': 10422, 'message': exc_str, 'data': None}
        return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = perf_counter()
    response = await call_next(request)
    process_time = perf_counter() - start_time
    response.headers["X-Process-Time"] = str(f'{process_time:0.4f} sec')
    return response


@app.get("/health", description='Health check to see if server is responding as expected.', tags=['Technical'])
def health():
    try:
        return {'status': 'up', 'version': APP_VERSION}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    '/chat',
    name='Text chatting.',
    description='Servicing chatting api.',
)
def chat(user_input: TextItem):
    # Initialize conversation memory and chain
    generated_response = get_response(user_input.history, user_input.text)

    return {
        'output': generated_response.to_dict()['choices'][-1]['message']['content']
    }


@app.post(
    '/recommend',
    name='Room recommendation.',
    description='Servicing chatting api.',
)

@app.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    r = MessagingResponse()
    media = request.form.get("MediaUrl0")
    msg_type = request.form.get("MediaContentType0")

    if msg_type == "audio/ogg; codecs=opus" and media:
        response = await process_voice_input(media)
        r.message(response)
    else:
        r.message("Please send a voice message.")
    
    return str(r)

async def process_voice_input(url: str) -> str:
    # Download the voice message
    r = requests.get(url)
    with open('voice_message.oga', 'wb') as f:
        f.write(r.content)

    # Convert the voice message to WAV
    # You'll need to use 'ffmpeg' or a similar tool to convert the file

    # Process the WAV file with SpeechRecognition
    recognizer = sr.Recognizer()
    with sr.AudioFile('voice_message_converted.wav') as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand your voice message."
    except sr.RequestError:
        return "An error occurred while processing your voice message."

    # Send the transcribed text to the FastAPI backend
    response = requests.post('http://chatbot_fastapi:5300/endpoint', json={"text": text})
    return response.text


# class AudioMessage(BaseModel):
    # sender: str
    # audio: bytes

# @app.post("/audio")
# async def receive_audio(audio_message: AudioMessage):
    # # Handle incoming audio message
    # sender = audio_message.sender
    # audio_data = audio_message.audio
#     
    # # Convert audio to text using a speech-to-text library like `SpeechRecognition`
    # # You can install the `SpeechRecognition` library via pip:
    # # `pip install SpeechRecognition`
#     
    # r = sr.Recognizer()
    # with sr.AudioFile(audio_data) as source:
        # audio_text = r.recognize_google(source)
#     Reach out to us ￼


def recommend(user_input: BookingItem):
    logging.warning(
        [BOOKINGS_CACHE, BOOKING_REQUEST]
    )
    if not BOOKINGS_CACHE:
        if all(required in BOOKING_REQUEST for required in [
            'FULL_NAME', 'START_DATE', 'END_DATE', 'CITY', 'BUDGET', 'GUEST_COUNT'
        ]):
            app.booking_demo_history, answer, app.interaction_count = recommend_booking(
                app.booking_demo_history,
                user_input.text, app.interaction_count, BOOKING_CHAIN, BOOKING_REQUEST,
                REDIS_CONNECTOR,
                city_code=CITY_MAPPING.get(BOOKING_REQUEST['CITY'].title())
            )
            logging.warning(user_input.text)
            logging.warning(answer)
            logging.warning(app.booking_demo_history)
            try:
                json_entities_string = re.findall(r'{.+}', answer, flags=re.MULTILINE | re.DOTALL)[0]
            except Exception as e:
                json_entities_string = '{}'

            entity_dict = literal_eval(json_entities_string)

            logging.warning(entity_dict)
            if 'ANSWER' in entity_dict:
                answer = entity_dict['ANSWER']
            else:
                answer = answer.split('{', 1)[0].strip()

            if entity_dict.get('USER_CONFIRMED_CHOICE'):
                BOOKINGS_CACHE['id'] = entity_dict['LISTING_ID']
                BOOKINGS_CACHE['city'] = BOOKING_REQUEST['CITY']
                BOOKINGS_CACHE['name'] = BOOKING_REQUEST['FULL_NAME']
                BOOKINGS_CACHE['dates:'] = BOOKING_REQUEST['START_DATE'] + '-' + BOOKING_REQUEST['END_DATE']
                booking_url = 'https://book.tripath.es/instance/' \
                              f'?check_in={BOOKING_REQUEST["START_DATE"]}' \
                              f'&check_out={BOOKING_REQUEST["END_DATE"]}' \
                              f'&guest={BOOKING_REQUEST["GUEST_COUNT"]}&' \
                              f'adult_guest={BOOKING_REQUEST["GUEST_COUNT"]}&child_guest=0' \
                              '&extra_options%5B0%5D=Utilities%7C50%7Cper_night' \
                              f'&listing_id={entity_dict["LISTING_ID"]}' \
                              '&guest_message=URL%20Provided%20by%20Tripath'
                answer = answer + f' The link for final confirmation for your booking is: {booking_url}.'
                app.booking_demo_history = []
        else:
            logging.warning('asking for entities')
            entity_dict_string = openai_chat_completion_ner_response(user_input.text)
            if entity_dict_string:
                entity_dict = literal_eval(entity_dict_string)
            else:
                entity_dict = []

            logging.warning(entity_dict)

            for key in entity_dict:
                if entity_dict[key]:
                    BOOKING_REQUEST[key] = entity_dict[key]
            logging.warning(BOOKING_REQUEST)
            if len(list(BOOKING_REQUEST)) == 6:
                booking_demo_history, answer = get_location_recommendations_response(
                    [], ' I got a booking in city ' + BOOKING_REQUEST['CITY'].title()
                )
                logging.warning(answer)
                try:
                    json_entities_string = re.findall(r'{.+}', answer, flags=re.MULTILINE | re.DOTALL)[0]
                except Exception:
                    json_entities_string = '{}'

                entity_dict = literal_eval(json_entities_string)
                logging.warning(entity_dict)
                if 'ANSWER' in entity_dict:
                    answer = entity_dict['ANSWER']
                else:
                    answer = answer.split('{', 1)[0].strip()

            else:
                answer, app.booking_demo_history = ask_for_booking_details(
                    app.booking_demo_history, user_input.text, BOOKING_REQUEST
                )
                logging.warning(answer)
                logging.warning(app.booking_demo_history)

    else:
        if not app.booking_demo_history:
            overview = 'Your apartment was booked already. Your listing overview: ' + str(BOOKINGS_CACHE) + '\n\n'
            app.booking_demo_history, answer = ask_about_general_requirements_response(
                app.booking_demo_history, 'I booked an accomBOOKING_REQUEST')
            app.booking_demo_history, answer = ask_about_general_requirements_response(
                app.booking_demo_history, user_input.text
            )

        if overview:
            answer = overview + answer

    return {
        'output': answer
    }
