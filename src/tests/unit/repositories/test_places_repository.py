import pytest
import pytest_asyncio
from sqlalchemy import insert

from repositories.places_repository import PlacesRepository
from tests.unit.repositories.test_repository_base import TestRepositoryBase


@pytest.mark.usefixtures("session")
class TestPlacesRepository(TestRepositoryBase):
    """
    Тестирование репозитория для списка любимых мест.
    """

    @pytest_asyncio.fixture
    async def repository(self, session):
        """
        Фикстура объекта тестируемого репозитория.

        :param session: Фикстура подключения к БД.
        :return:
        """

        yield PlacesRepository(session)

    @pytest.mark.asyncio
    async def test_find(self, repository, fixture_place):
        """
        Тестирование метода поиска записи по первичному ключу.

        :param repository: Фикстура объекта тестируемого репозитория.
        :param fixture_place: Фикстура объекта любимого места.
        :return:
        """

        # формирование данных для создания записи
        values = fixture_place.dict(exclude_none=True)
        # формирование запроса для создания записи
        statement = (
            insert(repository.model).values(values).returning(repository.model.id)
        )
        # выполнение запроса и получение первичного ключа созданной записи
        primary_key = (await repository.session.execute(statement)).fetchone().id

        # поиск созданного объекта в базе данных через метод репозитория
        created_object = await repository.find(primary_key)

        # тестирование полученного результата
        await self.assert_object(created_object, values)
