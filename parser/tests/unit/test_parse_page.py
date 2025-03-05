import pytest
from lxml import html
from utils.get_xml_form_data import parse_page

@pytest.mark.asyncio
async def test_parse_page():
    """
    Проверить, что функция parse_page корректно извлекает ссылки
    на печатные формы из переданного HTML-контента.

    Тест проверяет, что:
    1. Функция parse_page извлекает все ссылки на печатные формы
    (теги <a> с соответствующими href) из HTML-контента.
    2. Функция возвращает список строк с правильными ссылками.
    """
    raw_page = "<html><body><a href='/epz/order/notice/printForm/view.html?regNumber=12345'>link</a></body></html>"
    
    result = await parse_page(raw_page)

    assert result == ['/epz/order/notice/printForm/view.html?regNumber=12345']
