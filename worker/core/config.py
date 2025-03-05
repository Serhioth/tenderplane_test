from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Класс для хранения настроек приложения."""
  
    # Настройки приложения
    DEBUG: bool = False

    # Настройки брокера
    REDIS_QUEUE_NAME: str = "urls_queue"

    # Настройки для Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    @property
    def REDIS_URL(self) -> str:
        """Динамически генерируемая ссылка для содединения с Redis."""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    @property
    def CELERY_BROKER_URL(self) -> str:
        """Динамически генерируемая ссылка для брокера Celery."""
        return self.REDIS_URL

    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        """Динамически генерируемая ссылка для Celery backend."""
        return self.REDIS_URL

    class Config:
        env_file = ".env.worker"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
