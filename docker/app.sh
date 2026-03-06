#!/bin/bash
alembic upgrade head
exec gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:${PORT:-8000}