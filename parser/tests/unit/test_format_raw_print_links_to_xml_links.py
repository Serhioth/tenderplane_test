import pytest

from parser.core.config import settings
from utils.get_xml_form_data import format_raw_print_links_to_xml_links

def test_format_raw_print_links_to_xml_links():
    """
    Проверить, что функция format_raw_print_links_to_xml_links
    корректно форматирует переданные в неё ссылки.
    
    Тест проверяет что:
    1. Функция корректно форматирует переданные ссылки.
    2. Функция возвращает результат для каждой переданной ссылки.
    """
    raw_links = [
        "/epz/order/notice/printForm/view.html?regNumber=12345",
        "/epz/order/notice/printForm/view.html?regNumber=67890"
    ]

    result = format_raw_print_links_to_xml_links(raw_links)

    expected_result = [
        f"{settings.ROOT_URL}/epz/order/notice/printForm/viewXml.html?regNumber=12345",
        f"{settings.ROOT_URL}/epz/order/notice/printForm/viewXml.html?regNumber=67890"
    ]
    assert result == expected_result
