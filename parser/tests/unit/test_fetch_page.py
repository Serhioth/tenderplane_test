import pytest
from unittest import mock

from utils.get_xml_form_data import fetch_page


@pytest.mark.asyncio
async def test_fetch_page_success():
    """
    Проверить, что страница успешно получена,
    и результат соответствует ожидаемому.

    Тест проверяет, что:
    1. Функция fetch_page выполняет HTTP-запрос
    с правильными параметрами (URL, заголовки, параметры, тайм-аут).
    2. Функция возвращает ожидаемый текст страницы, если запрос успешен.
    """
    mock_response = mock.AsyncMock()
    mock_response.text = "<html></html>"
    mock_response.raise_for_status = mock.AsyncMock()
    
    mock_client = mock.AsyncMock()
    mock_client.get = mock.AsyncMock(return_value=mock_response)
    
    result = await fetch_page(mock_client, "http://example.com", 1)
    
    mock_client.get.assert_called_once_with(
        "http://example.com",
        headers=mock.ANY,
        params={"fz44": "on", "pageNumber": 1},
        timeout=30
    )
    assert result == "<html></html>"
