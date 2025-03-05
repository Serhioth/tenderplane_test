import pytest


@pytest.fixture
def celery_app(celery_app):
    """
    Fixture для настройки и тестирования приложения Celery.
    """
    celery_app.conf.update(
        CELERY_TASK_ALWAYS_EAGER=True,
    )
    return celery_app


@pytest.fixture
def celery_worker(celery_worker):
    """
    Fixture для запуска Celery worker для тестов.
    """
    return celery_worker
