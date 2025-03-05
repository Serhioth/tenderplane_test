from celery import Celery

from core.config import settings


celery_app = Celery(
    'producer',
    broker=settings.CELERY_BROKER_URL,
)
