FROM python:3.11

WORKDIR /app
COPY . .
CMD celery -A celery_app.celery_email.celery_app worker --loglevel=INFO -P gevent
