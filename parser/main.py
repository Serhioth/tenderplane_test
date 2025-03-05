import asyncio
import traceback

from core.config import settings
from core.logger import configure_logger
from utils import (
    get_xml_links_data,
    send_message,
)

logger = configure_logger(__name__)


async def fetch_and_process_urls():
    """Получить урл-адреса из файла и асинхронно их обработать."""
    try:
        xml_links_data = await get_xml_links_data(
            request_url=settings.ROOT_URL + settings.SEARCH_RESULT_PATH,
            pages_number=settings.PAGES_NUMBER,
        )
        await send_message(xml_links_data)
    except Exception as e:
        logger.error(f"Error fetching and processing URLs: {e}\n{traceback.format_exc()}")


async def main():
    await fetch_and_process_urls()


if __name__ == "__main__":
    asyncio.run(main())
