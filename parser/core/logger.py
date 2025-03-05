import logging
import sys

from core.config import settings


def configure_logger(name: str) -> logging.Logger:
    """Настройка логгера."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG) if settings.DEBUG else logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Хэндлер для вывода информации в консоль
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger
