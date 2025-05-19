#!/bin/sh

celery -A backend.celery_app.celery_email.celery_app worker -l info --concurrency=2 &
celery -A  backend.celery_app.celery_email.celery_app flower -l info &
uvicorn backend.main:app --host 0.0.0.0 --reload
