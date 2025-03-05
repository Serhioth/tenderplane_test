import asyncio

from celery import Task
from core.logger import configure_logger
from utils import process_xml_print_form_urls

logger = configure_logger(__name__)


class MyTask(Task):
    """
    Класс задачи, наследующийся от celery.Task
    """

    def run(self, data: dict[str, str]):
        """
        Запуск задачи, которая обрабатывает URL и выводит результат.
        """
        result_data = process_xml_print_form_urls(data)

        for key, value in result_data.items():
            logger.info(f"{key}: {value}")
