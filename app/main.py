import os
import logging

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from time import perf_counter


from app.conversation_manager.context_memory import get_response
from app.pydantic_models import TextItem

APP_VERSION = os.environ.get('APP_VERSION', None)

app = FastAPI(
    root_path=os.environ.get('FAST_API_ROOT_PATH', ''),
    title="REST API for interacting with chatGPT model.",
    version=APP_VERSION
)

logging.info('☺ ☺ ☺ waiting for input ☺ ☺ ☺')


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
    name='Text clustering.',
    description='Servicing chatting api.',
)
def chat(user_input: TextItem):
    # Initialize conversation memory and chain
    generated_response = get_response(user_input.history, user_input.text)

    return {
        'output': generated_response.to_dict()['choices'][-1]['message']['content']
    }
