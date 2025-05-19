from celery import Celery

celery_app = Celery(
    main="backend.celery_app.celery_email",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)
celery_app.autodiscover_tasks(
    packages=["backend.celery_app.celery_email.tasks"]
)
