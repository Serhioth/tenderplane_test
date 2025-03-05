import asyncio

import httpx
from lxml import html

from core.config import settings
from core.logger import configure_logger

logger = configure_logger(__name__)


async def fetch_page(client, request_url, page):
    """Получить данные страницы."""
    response = await client.get(
        request_url,
        headers=settings.HEADERS,
        params={"fz44": "on", "pageNumber": page},
        timeout=30
    )
    response.raise_for_status()
    return response.text


async def get_raw_pages(request_url: str, pages_number: int):
    """
    Получить HTML-страницы параллельно.
    """
    async with httpx.AsyncClient() as client:
        tasks = [fetch_page(client, request_url, page) for page in range(1, pages_number + 1)]
        return await asyncio.gather(*tasks)


async def parse_page(raw_page: str):
    """Асинхронно парсит ссылки из одной страницы."""
    tree = html.fromstring(raw_page)
    return tree.xpath('//a[contains(@href, "epz/order/notice/printForm/view.html")]/@href')


async def parse_raw_print_form_links_from_raw_pages(raw_pages: list[str]):
    """
    Получить ссылки на печатные xml-формы.
    Обрабатывает страницы параллельно.
    """
    tasks = [parse_page(page) for page in raw_pages]
    results = await asyncio.gather(*tasks)
    return [link for links in results for link in links]


def format_raw_print_links_to_xml_links(raw_print_links: list[str]):
    """Форматировать ссылки на печатные xml-формы."""
    return [
        settings.ROOT_URL + link.replace("view.html", "viewXml.html")
        for link in raw_print_links
    ]


async def get_xml_data(client, xml_link: str):
    """Получить данные xml-формы."""
    logger.info(f"Обработка ссылки: {xml_link}")
    base_url, _, reg_number = xml_link.partition("?regNumber=")
    if not reg_number:
        logger.error(f"Неверный формат ссылки: {xml_link}")
        return xml_link, None
    try:
        response = await client.get(
            base_url,
            headers=settings.HEADERS,
            params={"regNumber": reg_number},
            timeout=30
        )
        response.raise_for_status()
        return xml_link, response.text
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error for {xml_link}: {e}")
        return xml_link, None
    except httpx.RequestError as e:
        logger.error(f"Request error for {xml_link}: {e}")
        return xml_link, None
    except Exception as e:
        logger.error(f"Unexpected error for {xml_link}: {e}")


async def get_xml_data_parallel(xml_links: list[str]):
    """
    Получить данные xml-форм параллельно и вернуть словарь {xml_link: data}.
    """
    async with httpx.AsyncClient() as client:
        tasks = [get_xml_data(client, link) for link in xml_links]
        results = await asyncio.gather(*tasks)
        return {link: data for link, data in results}


async def get_xml_links_data(request_url: str, pages_number: int):
    """
    Получить ссылки на печатные xml-формы.
    """
    raw_pages = await get_raw_pages(request_url, pages_number)
    raw_print_links = await parse_raw_print_form_links_from_raw_pages(raw_pages)
    xml_links = format_raw_print_links_to_xml_links(raw_print_links)
    xml_links_data = await get_xml_data_parallel(xml_links)
    return xml_links_data
