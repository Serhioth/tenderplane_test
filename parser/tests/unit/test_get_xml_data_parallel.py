import pytest
from unittest import mock

from utils.get_xml_form_data import get_xml_data_parallel

@pytest.mark.asyncio
async def test_get_xml_data_parallel():
    """
    Проверить функцию get_xml_data_parallel.

    Этот тест имитирует функцию get_xml_data,
    возвращающую фиксированную XML-строку.
    Затем вызывается функция get_xml_data_parallel со списком XML-ссылок
    и проверяется, содержит ли возвращаемый словарь ожидаемые XML-строки
    для каждой ссылки.
    """
    mock_get_xml_data = mock.patch(
        "utils.get_xml_form_data.get_xml_data",
        side_effect=lambda _, url: (url, "<xml></xml>")
    ).start()

    xml_links = [
        "http://example.com?regNumber=12345",
        "http://example.com?regNumber=67890"
    ]

    result = await get_xml_data_parallel(xml_links)

    assert result == {
        "http://example.com?regNumber=12345": "<xml></xml>",
        "http://example.com?regNumber=67890": "<xml></xml>"
    }
    mock_get_xml_data.assert_any_call(
        mock.ANY,
        "http://example.com?regNumber=12345"
    )
    mock_get_xml_data.assert_any_call(
        mock.ANY,
        "http://example.com?regNumber=67890"
    )
    mock_get_xml_data.stop()
