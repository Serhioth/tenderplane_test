from unittest.mock import patch

from utils.process_xml_print_form_link import (
    process_xml_print_form_urls
)


@patch('utils.process_xml_print_form_link.parse_xml')
def test_process_xml_print_form_urls(mock_parse_xml):
    """
    Проверить, что функция process_xml_print_form_urls, корректно 
    обрабатывает несколько ссылок с XML-данными.

    Тест проверяет что:
    1. Для каждой ссылки вызывается функция parse_xml, которая должна вернуть правильный 
       результат в виде ссылки и даты публикации.
    2. Результат работы process_xml_print_form_urls должен быть словарем, где ключами 
       являются ссылки, а значениями — даты публикации.
    """
    def mock_parse(link, response):
        if link == 'http://example1.com':
            return 'http://example1.com', '2025-03-05T12:00:00'
        elif link == 'http://example2.com':
            return 'http://example2.com', '2025-03-05T12:00:00'
        return link, None

    mock_parse_xml.side_effect = mock_parse

    xml_form_data = {
        'http://example1.com': '<xml>...</xml>',
        'http://example2.com': '<xml>...</xml>',
    }
    
    result = process_xml_print_form_urls(xml_form_data)

    assert result == {
        'http://example1.com': '2025-03-05T12:00:00',
        'http://example2.com': '2025-03-05T12:00:00',
    }
