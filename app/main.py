import os
import re
import logging

from ast import literal_eval

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from time import perf_counter


from app.conversation_manager.context_memory import (
    get_response, get_booking_chain, openai_chat_completion_ner_response
)
from app.conversation_manager.conversation_contexts import recommend_booking, ask_for_booking_details
from app.pydantic_models import TextItem

from app.data.data_loaders import get_room_dataframe
from app.vectorizers.sentence_transformer import get_data_vectors
from app.redis_manager.redis_connector import get_redis_connector, create_flat_index, load_vectors


APP_VERSION = os.environ.get('APP_VERSION', None)

app = FastAPI(
    root_path=os.environ.get('FAST_API_ROOT_PATH', ''),
    title="REST API for interacting with chatGPT model.",
    version=APP_VERSION
)

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
def recommend(user_input: TextItem):
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
                app.booking_demo_history, answer, app.interaction_count = recommend_booking(
                    [],
                    user_input.text, app.interaction_count, BOOKING_CHAIN, BOOKING_REQUEST,
                    REDIS_CONNECTOR,
                    city_code=CITY_MAPPING.get(BOOKING_REQUEST['CITY'].title())
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
                    answer += f' The link for final confirmation for your booking is: {booking_url}.'
            else:
                answer, app.booking_demo_history = ask_for_booking_details(
                    app.booking_demo_history, user_input.text, BOOKING_REQUEST
                )
                logging.warning(answer)
                logging.warning(app.booking_demo_history)

    else:
        answer = 'Your apartment was booked already. Your listing id is: ' + str(BOOKINGS_CACHE)

    return {
        'output': answer
    }
