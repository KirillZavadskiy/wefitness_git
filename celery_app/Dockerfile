FROM python:3.11

WORKDIR /celery_app
COPY . .
CMD celery -A celery_email.celery_app worker --loglevel=INFO -P gevent
