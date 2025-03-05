import pytest
from unittest import mock

from utils.get_xml_form_data import get_raw_pages

@pytest.mark.asyncio
async def test_get_raw_pages():
    """
    Проверить, что функция get_raw_pages вызывает fetch_page дважды
    с правильными параметрами для двух страниц.

    Тест проверяет, что:
    1. Функция get_raw_pages возвращает два элемента.
    2. Функция fetch_page вызывается дважды,
    каждый раз с ожидаемым URL и номером страницы.
    """
    mock_fetch_page = mock.patch(
        "utils.get_xml_form_data.fetch_page",
        return_value="<html></html>"
    ).start()

    # Вызов функции
    result = await get_raw_pages("http://example.com", 2)

    # Проверки
    assert len(result) == 2
    mock_fetch_page.assert_any_call(mock.ANY, "http://example.com", 1)
    mock_fetch_page.assert_any_call(mock.ANY, "http://example.com", 2)
    mock_fetch_page.stop()
