import pytest
import redis

from core.config import settings


@pytest.fixture(scope="function")
def redis_client():
    """
    Фикстура для клиента Redis.
    """
    client = redis.StrictRedis.from_url(settings.REDIS_URL)
    client.flushdb()

    yield client

    client.flushdb()
