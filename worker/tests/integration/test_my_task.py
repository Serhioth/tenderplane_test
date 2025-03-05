import pytest
from unittest.mock import patch
from tasks.tasks import MyTask
from utils import process_xml_print_form_urls


@patch('tasks.tasks.process_xml_print_form_urls')
def test_my_task(mock_process_xml, celery_worker):
    """
    Тестируем Celery таск MyTask.
    """
    # Подготовим входные данные
    input_data = {
        "url1": "<xml><commonInfo><publishDTInEIS>2025-03-05</publishDTInEIS></commonInfo></xml>",
        "url2": "<xml><commonInfo><publishDTInEIS>2025-03-06</publishDTInEIS></commonInfo></xml>"
    }
    
    # Мокаем поведение функции process_xml_print_form_urls, чтобы она возвращала ожидаемые данные
    mock_process_xml.return_value = {
        "url1": "2025-03-05",
        "url2": "2025-03-06"
    }

    # Запускаем таск и ожидаем результат
    result = MyTask().run(input_data)

    # Проверяем, что функция process_xml_print_form_urls была вызвана с правильными аргументами
    mock_process_xml.assert_called_once_with(input_data)
    
    # Вы можете также добавить проверку других частей выполнения таска
    assert result is None  # Если таск не возвращает значений, проверяем, что он не возвращает ошибку.
