import pytest
from unittest import mock
from utils.get_xml_form_data import get_xml_links_data

@pytest.mark.asyncio
async def test_get_xml_links_data():
    """
    Проверить, что функция get_xml_links_data, правильно обрабатывает
    данные с различных этапов обработки и возвращает ожидаемый результат.
    
    В тесте проверяется, что результат выполнения функции get_xml_links_data
    совпадает с ожидаемым словарем, содержащим XML-данные для каждой ссылки.
    """
    mock_get_raw_pages = mock.patch(
        "utils.get_xml_form_data.get_raw_pages",
        return_value=["<html></html>"]
    ).start()
    
    mock_parse_raw_print_form_links_from_raw_pages = mock.patch(
        "utils.get_xml_form_data.parse_raw_print_form_links_from_raw_pages",
        return_value=["link1"]
    ).start()
    
    mock_format_raw_print_links_to_xml_links = mock.patch(
        "utils.get_xml_form_data.format_raw_print_links_to_xml_links",
        return_value=["http://example.com/xml"]
    ).start()
    
    mock_get_xml_data_parallel = mock.patch(
        "utils.get_xml_form_data.get_xml_data_parallel",
        return_value={"http://example.com/xml": "<xml></xml>"}
    ).start()

    request_url = "http://example.com"
    pages_number = 1

    result = await get_xml_links_data(request_url, pages_number)

    assert result == {"http://example.com/xml": "<xml></xml>"}

    mock_get_raw_pages.stop()
    mock_parse_raw_print_form_links_from_raw_pages.stop()
    mock_format_raw_print_links_to_xml_links.stop()
    mock_get_xml_data_parallel.stop()
