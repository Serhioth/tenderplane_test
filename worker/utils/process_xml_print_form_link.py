import asyncio

import xmltodict

from core.logger import configure_logger

logger = configure_logger(__name__)


def parse_xml(link: str, response: str) -> tuple[str, str | None]:
    """Парсинг XML для Celery."""
    if not response:
        return link, None
    try:
        xml_dict = xmltodict.parse(response)  # Синхронный вызов
        root_value = xml_dict.get(next(iter(xml_dict), {}), {})
        common_info = root_value.get("commonInfo", {})
        publish_dt = common_info.get("publishDTInEIS")

        if not publish_dt:
            logger.warning(f"publishDTInEIS not found for {link}")

        return link, publish_dt
    except Exception as e:
        logger.error(f"Error parsing XML for {link}: {e}")
        return link, None


def process_xml_print_form_urls(
    xml_form_data: dict[str, str],
) -> dict[str, str | None]:
    """Обработка XML для Celery."""
    logger.info("Начало обработки ссылок на печатные XML-формы")

    results = [
        parse_xml(link, response) for link, response in xml_form_data.items()
    ]
    return dict(results)
