from pydantic import Json
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Класс для хранения настроек приложения."""
  
    # Настройки приложения
    DEBUG: bool = False
    
    # Настройки парсера
    HEADERS: Json[dict] = {
        "Content-Type": "application/json; charset=utf-8",
        "Referer": "https://zakupki.gov.ru/",
        "Sec-CH-UA": '"Not A(Brand";v="8", "Chromium";v="132", "YaBrowser";v="25.2", "Yowser";v="2.5"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"Windows"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 YaBrowser/25.2.0.0 Safari/537.36",
    }
    ROOT_URL: str = "https://zakupki.gov.ru"
    SEARCH_RESULT_PATH: str = "/epz/order/extendedsearch/results.html"
    PAGES_NUMBER: int = 2

    # Настройки брокера
    REDIS_QUEUE_NAME: str = "urls_queue"

    # Настройки для Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @property
    def REDIS_URL(self) -> str:
        """Ссылка для содединения с Redis."""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    @property
    def CELERY_BROKER_URL(self) -> str:
        """Динамически генерируемая ссылка для брокера Celery."""
        return self.REDIS_URL

settings = Settings()
