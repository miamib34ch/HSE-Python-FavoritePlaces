from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type, Union

from pydantic.main import BaseModel
from sqlalchemy import Column, insert, update
from sqlalchemy.engine import CursorResult, Result, Row
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select
from sqlmodel.sql.expression import SelectOfScalar


class BaseRepository(ABC):
    """
    Базовый абстрактный класс репозитория.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Инициализация репозитория.

        :param session: Объект сессии для взаимодействия с БД
        """

        self.session = session

    @property
    @abstractmethod
    def model(self) -> Type[SQLModel]:
        """
        Модель таблицы.
        """

    def get_attr(self, attr: str) -> Column:
        """
        Получение атрибута модели по наименованию.

        :param attr:
        :return:
        """

        return getattr(self.model, attr)

    def _select(self, **kwargs: Any) -> SelectOfScalar:
        """
        Формирование выборки с условиями.

        :param kwargs: Аргументы для формирования условий выборки.
        :return:
        """

        query = select(self.model)
        condition = None
        for attr, value in kwargs.items():
            expression = self.get_attr(attr) == value
            if condition is not None:
                condition &= expression
            else:
                condition = expression

        if condition is not None:
            query = query.where(condition)

        return query

    async def find(self, primary_key: int) -> Optional[Row]:
        """
        Поиск объекта по его идентификатору.

        :param primary_key: Идентификатор объекта
        :return:
        """

        cursor = await self.session.execute(self._select(id=primary_key))
        return cursor.scalar()

    async def find_all_by(
        self,
        *,
        limit: int,
        order_by: Optional[Any] = None,
        offset: Optional[int] = 0,
        **kwargs: Any,
    ) -> list:
        """
        Поиск объектов по заданным параметрам.

        :param offset: Смещение элементов
        :param order_by: Сортировка (по умолчанию - ID)
        :param limit: Лимит на количество элементов в выборке
        :param kwargs: Условия для выборки
        :return:
        """

        order_by = order_by or self.get_attr("id")
        query = self._select(**kwargs).order_by(order_by).limit(limit).offset(offset)
        cursor = await self.session.execute(query)

        return cursor.scalars().all()

    async def create_model(self, model: Union[Dict, BaseModel]) -> Optional[int]:
        """
        Создание записи.

        :param model: Данные модели для создания.
        :return:
        """

        values = (
            model
            if isinstance(model, dict)
            else model.dict(exclude={"id"}, exclude_none=True)
        )
        cursor: Result = await self.session.execute(
            insert(self.model).values(**values).returning(self.get_attr("id"))
        )

        result = cursor.fetchone()

        return result.id if result else None

    async def update_model(self, primary_key: int, **kwargs: Any) -> Optional[int]:
        """
        Обновление записи.

        :param primary_key: Первичный ключ
        :param kwargs: Атрибуты и их значения
        :return:
        """

        statement = (
            update(self.model)
            .where(self.get_attr("id") == primary_key)
            .values(**kwargs)
        )

        result: CursorResult = await self.session.execute(statement)  # type: ignore

        return result.rowcount if result else None

    async def delete_by(self, **kwargs: Any) -> None:
        """
        Удаление записи по переданному условию.

        :param kwargs: Значения атрибутов
        :return:
        """

        statement = self._select(**kwargs)
        result = await self.session.execute(statement)
        try:
            row = result.scalar_one()
            await self.session.delete(row)

            return row.id
        except NoResultFound:

            return None
