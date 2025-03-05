import pytest
from unittest import mock

import httpx

from utils.get_xml_form_data import get_xml_data

@pytest.mark.asyncio
async def test_get_xml_data_success():
    """
    Проверить, что функция get_xml_data возвращает корректный результат
    при успешном запросе к переданной ссылке на печатную xml-форму.
    
    Тест проверяет что:
    1. Функция вызывается 1 раз для переданной ссылки.
    2. Функция возвращает корректный результат
    при успешном запросе к переданной ссылке.
    """
    mock_response = mock.AsyncMock()
    mock_response.text = "<xml></xml>"
    mock_response.raise_for_status = mock.AsyncMock()

    mock_client = mock.AsyncMock()
    mock_client.get.return_value = mock_response

    xml_link = "http://example.com?regNumber=12345"

    result = await get_xml_data(mock_client, xml_link)

    mock_client.get.assert_called_once_with(
        "http://example.com",
        headers=mock.ANY,
        params={"regNumber": "12345"},
        timeout=30
    )
    assert result == (xml_link, "<xml></xml>")

@pytest.mark.asyncio
async def test_get_xml_data_error():
    """
    Проверить, что функция get_xml_data возвращает корректный результат
    при ошибке запроса к переданной ссылке на печатную xml-форму.

    Тест проверяет что:
    1. Функция вызывается 1 раз для переданной ссылки.
    2. Функция возвращает корректный результат
    при ошибке запроса к переданной ссылке.
    """
    mock_client = mock.AsyncMock()
    mock_client.get.side_effect = httpx.RequestError("Test error", request=None)

    xml_link = "http://example.com?regNumber=12345"

    result = await get_xml_data(mock_client, xml_link)

    assert result == (xml_link, None)
