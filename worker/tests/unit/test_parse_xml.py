from unittest.mock import patch

from utils.process_xml_print_form_link import parse_xml


@patch('utils.process_xml_print_form_link.xmltodict.parse')
def test_parse_xml_success(mock_parse):
    """
    Проверить, что функция parse_xml корректно парсит XML и возвращает правильную дату публикации.

    Тест проверяет, что:
    1. Функция успешно парсит переданный XML и извлекает значение из тега 'publishDTInEIS'.
    2. Возвращаемое значение link соответствует переданному URL.
    3. Возвращаемое значение publish_dt соответствует извлечённой дате.
    """
    mock_parse.return_value = {
        'root': {
            'commonInfo': {
                'publishDTInEIS': '2025-03-05T12:00:00'
            }
        }
    }

    link, publish_dt = parse_xml('http://example.com', '<xml>...</xml>')

    assert link == 'http://example.com'
    assert publish_dt == '2025-03-05T12:00:00'


@patch('utils.process_xml_print_form_link.xmltodict.parse')
def test_parse_xml_publishDTInEIS_not_found(mock_parse):
    """
    Проверить, что функция parse_xml корректно обрабатывает отсутствие тега 'publishDTInEIS'.

    Тест проверяет, что:
    1. При отсутствии тега 'publishDTInEIS' в XML генерируется предупреждающее сообщение.
    2. Функция возвращает правильный URL и None для даты публикации.
    """
    mock_parse.return_value = {
        'root': {
            'commonInfo': {}
        }
    }

    with patch('utils.process_xml_print_form_link.logger.warning') as mock_warning:
        link, publish_dt = parse_xml('http://example.com', '<xml>...</xml>')
        mock_warning.assert_called_with("publishDTInEIS not found for http://example.com")
    
    assert link == 'http://example.com'
    assert publish_dt is None


@patch('utils.process_xml_print_form_link.xmltodict.parse')
def test_parse_xml_exception(mock_parse):
    """
    Проверить, что функция parse_xml корректно обрабатывает исключения при парсинге XML.

    Тест проверяет, что:
    1. При возникновении исключения в процессе парсинга генерируется ошибка.
    2. Функция возвращает правильный URL и None для даты публикации.
    """
    mock_parse.side_effect = Exception('Parsing error')

    with patch('utils.process_xml_print_form_link.logger.error') as mock_error:
        link, publish_dt = parse_xml('http://example.com', '<xml>...</xml>')
        mock_error.assert_called_with("Error parsing XML for http://example.com: Parsing error")
    
    assert link == 'http://example.com'
    assert publish_dt is None


@patch('utils.process_xml_print_form_link.xmltodict.parse')
def test_parse_xml_empty_response(mock_parse):
    """
    Проверить, что функция parse_xml корректно обрабатывает пустой ответ.

    Тест проверяет, что:
    1. При получении пустого ответа функция возвращает правильный URL и None для даты публикации.
    """
    link, publish_dt = parse_xml('http://example.com', '')

    assert link == 'http://example.com'
    assert publish_dt is None
