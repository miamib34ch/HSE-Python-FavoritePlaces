import logging.config
from typing import Optional

from fastapi import Depends
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from clients.geo import LocationClient
from integrations.db.session import get_session
from integrations.events.producer import EventProducer
from integrations.events.schemas import CountryCityDTO
from models import Place
from repositories.places_repository import PlacesRepository
from schemas.places import PlaceUpdate
from settings import settings

logging.config.fileConfig("logging.conf")
logger = logging.getLogger()


class PlacesService:
    """
    Сервис для работы с информацией о любимых местах.
    """

    def __init__(self, session: AsyncSession = Depends(get_session)):
        """
        Инициализация сервиса.

        :param session: Объект сессии для взаимодействия с базой данных
        """

        self.session = session
        self.places_repository = PlacesRepository(session)

    async def get_places_list(self, limit: int) -> list[Place]:
        """
        Получение списка любимых мест.

        :param limit: Ограничение на количество элементов в выборке.
        :return:
        """

        return await self.places_repository.find_all_by(limit=limit)

    async def get_place(self, primary_key: int) -> Optional[Place]:
        """
        Получение объекта любимого места по его идентификатору.

        :param primary_key: Идентификатор объекта.
        :return:
        """

        return await self.places_repository.find(primary_key)

    async def create_place(self, place: Place) -> Optional[int]:
        """
        Создание нового объекта любимого места по переданным данным.

        :param place: Данные создаваемого объекта.
        :return: Идентификатор созданного объекта.
        """

        # обогащение данных путем получения дополнительной информации от API
        if location := await LocationClient().get_location(
            latitude=place.latitude, longitude=place.longitude
        ):
            place.country = location.alpha2code
            place.city = location.city
            place.locality = location.locality

        primary_key = await self.places_repository.create_model(place)
        await self.session.commit()

        # публикация события о создании нового объекта любимого места
        # для попытки импорта информации по нему в сервисе Countries Informer
        try:
            place_data = CountryCityDTO(
                city=place.city,
                alpha2code=place.country,
            )
            EventProducer().publish(
                queue_name=settings.rabbitmq.queue.places_import, body=place_data.json()
            )
        except ValidationError:
            logger.warning(
                "The message was not well-formed during publishing event.",
                exc_info=True,
            )

        return primary_key

    async def update_place(self, primary_key: int, place: PlaceUpdate) -> Optional[int]:
        """
        Обновление объекта любимого места по переданным данным.

        :param primary_key: Идентификатор объекта.
        :param place: Данные для обновления объекта.
        :return:
        """

        # при изменении координат – обогащение данных путем получения дополнительной информации от API
        # todo

        matched_rows = await self.places_repository.update_model(
            primary_key, **place.dict(exclude_unset=True)
        )
        await self.session.commit()

        # публикация события для попытки импорта информации
        # по обновленному объекту любимого места в сервисе Countries Informer
        # todo

        return matched_rows

    async def delete_place(self, primary_key: int) -> Optional[int]:
        """
        Удаление объекта любимого места по его идентификатору.

        :param primary_key: Идентификатор объекта.
        :return:
        """

        matched_rows = await self.places_repository.delete_by(id=primary_key)
        await self.session.commit()

        return matched_rows
