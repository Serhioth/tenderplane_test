from celery import Celery
from kombu import Queue, Exchange
from core.config import settings
from core.logger import configure_logger
from tasks.tasks import MyTask  # Импорт задачи

logger = configure_logger(__name__)

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    broker_connection_retry_on_startup=True,
)

# Убедитесь, что задача зарегистрирована в Celery
celery_app.register_task(MyTask())  # Регистрация задачи

# Настройка очереди
response_data_q_name = settings.REDIS_QUEUE_NAME

my_task_queue = Queue(
    name=response_data_q_name,
    exchange=Exchange(response_data_q_name, type="direct"),
    routing_key=response_data_q_name,
)

celery_app.conf.task_queues = (my_task_queue,)

celery_app.conf.update(
    enable_utc=True,
    timezone="UTC",
    task_default_queue=response_data_q_name,
    task_default_exchange="direct",
    task_default_routing_key="default",
)

# Проверка зарегистрированных задач
registered_task = celery_app.tasks

if registered_task:
    for task_name in registered_task:
        logger.info(f"Registered task: {task_name}")
else:
    logger.info("No registered tasks found.")
