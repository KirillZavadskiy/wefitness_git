from celery import Celery

# from celery_app.settings import BACKEND_CELERY, BROKER_CELERY

celery_app = Celery(
    main="celery_app.celery_email",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)
celery_app.autodiscover_tasks(packages=["celery_app.celery_email.tasks"])
