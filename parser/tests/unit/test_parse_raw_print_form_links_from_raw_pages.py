import pytest
from unittest import mock
from utils.get_xml_form_data import (
    parse_raw_print_form_links_from_raw_pages
)

@pytest.mark.asyncio
async def test_parse_raw_print_form_links_from_raw_pages():
    """
    Проверить, что функция parse_raw_print_form_links_from_raw_pages
    вызывает функцию parse_page корректное количество раз,
    по числу переданных страниц.
    
    Тест проверяет, что:
    1. Результат функции совпадает с ожидаемым списком ссылок.
    2. Функция parse_page была вызвана хотя бы один раз
    с переданным HTML-контентом.
    """
    mock_parse_page = mock.patch(
        "utils.get_xml_form_data.parse_page",
        return_value=["link1", "link2"]
    ).start()

    raw_pages = ["<html></html>", "<html></html>"]

    result = await parse_raw_print_form_links_from_raw_pages(raw_pages)

    assert result == ["link1", "link2", "link1", "link2"]
    mock_parse_page.assert_any_call("<html></html>")
    mock_parse_page.stop()
