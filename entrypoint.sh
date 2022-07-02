#!/bin/bash

APP_PORT=${PORT:-8080}

/opt/venv/bin/gunicorn -k uvicorn.workers.UvicornWorker src.app:app --bind "0.0.0.0:${APP_PORT}"