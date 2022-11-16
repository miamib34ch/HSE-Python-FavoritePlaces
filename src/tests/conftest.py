import pytest_asyncio
from httpx import AsyncClient
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from integrations.db.session import get_session
from main import app
from settings import settings


@pytest_asyncio.fixture
async def session():
    """
    Фикстура тестовой сессии для работы с базой данных.
    После тестирования изменения, сделанные в БД не сохраняются.

    :return:
    """

    db_engine = create_async_engine(settings.database_url, echo=True, future=True)
    connection = await db_engine.connect()
    transaction = await connection.begin()

    async_session = AsyncSession(bind=connection)
    await async_session.begin_nested()

    app.dependency_overrides[get_session] = lambda: async_session

    yield async_session

    await async_session.close()
    await transaction.rollback()
    await connection.close()


@pytest_asyncio.fixture
async def client():
    """
    Получение асинхронного клиента для осуществления запросов.

    :return:
    """

    yield AsyncClient(app=app, base_url=settings.base_url)


@pytest_asyncio.fixture
async def non_mocked_hosts():
    """
    Исключение запросов к приложению из процесса создания мок-объектов для запросов.
    Используется автоматически pytest_httpx.
    https://colin-b.github.io/pytest_httpx/

    :return:
    """

    yield ["localhost", "127.0.0.1", "0.0.0.0"]


@pytest_asyncio.fixture
async def event_producer_publish(mocker: MockerFixture):
    """
    Создание "заглушки" для метода EventProducer.publish().

    :param mocker: MockerFixture
    :return:
    """

    mocker.patch(
        "integrations.events.producer.EventProducer.publish", return_value=None
    )
