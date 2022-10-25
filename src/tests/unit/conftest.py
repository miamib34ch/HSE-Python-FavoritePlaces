import pytest_asyncio

from models import Place


@pytest_asyncio.fixture
async def fixture_place() -> Place:
    """
    Фикстура объекта любимого места.

    :return:
    """

    return Place(
        latitude=12.345,
        longitude=23.567,
        description="Тестовое описание",
    )
