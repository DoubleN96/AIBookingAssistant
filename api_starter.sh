#!/bin/sh
# gunicorn main:app --workers 4  --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:5300
uvicorn main:app --host 0.0.0.0 --port ${PORT}