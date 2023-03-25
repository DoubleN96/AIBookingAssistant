import os
import logging
import numpy as np

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from time import perf_counter


from app.conversation_manager.context_memory import get_response, get_booking_chain, booking_interact
from app.pydantic_models import TextItem

from app.data.data_loaders import get_room_dataframe
from app.vectorizers.sentence_transformer import get_data_vectors, NUMBER_PRODUCTS
from app.vectorizers.sentence_transformer import model as vectorizer
from app.redis_manager.redis_connector import get_redis_connector, create_flat_index, get_booking_query


APP_VERSION = os.environ.get('APP_VERSION', None)

app = FastAPI(
    root_path=os.environ.get('FAST_API_ROOT_PATH', ''),
    title="REST API for interacting with chatGPT model.",
    version=APP_VERSION
)

logging.info('☺ ☺ ☺ waiting for input ☺ ☺ ☺')

DATA = get_room_dataframe()
DATA_VECTORS = get_data_vectors(DATA)
REDIS_CONNECTOR = get_redis_connector('redis')

REDIS_CONNECTOR.flushall()
create_flat_index(
    REDIS_CONNECTOR,
    'item_keyword_vector',
    NUMBER_PRODUCTS,
    768,
    'COSINE'
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
    # Run the chain only specifying the input variable.
    keywords = BOOKING_CHAIN.run(user_input.text)

    top_k = 3
    # vectorize the query
    query_vector = vectorizer.encode(keywords).astype(np.float32).tobytes()
    params_dict = {"vec_param": query_vector}

    # Execute the query
    results = REDIS_CONNECTOR.ft().search(get_booking_query(top_k), query_params=params_dict)
    agent, answer = booking_interact(results, user_input.text)

    return {
        'output': answer, 'results': [item.__dict__ for item in results.docs]
    }
