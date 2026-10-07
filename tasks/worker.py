from celery import Celery
from config.settings import settings

celery_app = Celery(
    "email_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)


celery_app.autodiscover_tasks(["tasks"])
