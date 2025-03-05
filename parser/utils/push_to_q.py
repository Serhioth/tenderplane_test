from core.celery_app import celery_app
from core.config import settings
from core.logger import configure_logger


async def send_message(data: dict[str, str]):
    celery_app.send_task(
        'tasks.tasks.MyTask',
        args=[data],
        queue=settings.REDIS_QUEUE_NAME,
    )
