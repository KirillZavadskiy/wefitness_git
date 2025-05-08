from celery import Celery

from backend.settings import BACKEND_CELERY, BROKER_CELERY

celery_app = Celery(
    main="celery_app.celery_email",
    broker=BROKER_CELERY,
    backend=BACKEND_CELERY
)
celery_app.autodiscover_tasks(packages=["celery_app.celery_email.tasks"])
