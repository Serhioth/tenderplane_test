import pytest
from time import sleep
import base64
import json
from unittest import mock

from core.config import settings
from core.celery_app import celery_app
from utils import send_message


@pytest.mark.asyncio
async def test_send_message(redis_client):
    # Данные для теста
    data = {"key": "value"}

    # НЕ мокаем send_task, чтобы задача попала в Redis
    await send_message(data)
    
    # Пауза, чтобы Celery успел обработать задачу и задача попала в очередь
    sleep(1)

    # Получение задач из Redis очереди
    tasks = redis_client.lrange(settings.REDIS_QUEUE_NAME, 0, -1)
    
    # Проверка, что в очереди есть хотя бы одна задача
    assert len(tasks) > 0
    task_data = tasks[0]
    
    # Декодируем данные из очереди
    task_data_decoded = task_data.decode('utf-8')
    
    # Задачи Celery хранят данные в base64, так что нам нужно декодировать тело
    task_data_json = json.loads(task_data_decoded)
    body_base64 = task_data_json["body"]
    
    # Декодируем тело из base64
    body_decoded = base64.b64decode(body_base64).decode('utf-8')

    # Проверяем, что в теле задачи содержатся переданные данные
    assert '"key": "value"' in body_decoded  # Строковое представление данных
