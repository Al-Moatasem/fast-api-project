#!/bin/bash

RUN_HOST=${APP_HOST:-0.0.0.0}
RUN_PORT=${APP_PORT:-8000}

/opt/venv/bin/alembic upgrade heads

/opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm -k uvicorn.workers.UvicornWorker --bind "${RUN_HOST}:${RUN_PORT}" src.main:app --reload
