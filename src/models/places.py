from typing import Optional

from sqlmodel import Field, SQLModel

from models.mixins import TimeStampMixin


class Place(SQLModel, TimeStampMixin, table=True):
    """
    Модель для описания места.
    """

    id: Optional[int] = Field(title="Идентификатор", default=None, primary_key=True)
    latitude: float = Field(title="Широта")
    longitude: float = Field(title="Долгота")
    description: str = Field(title="Описание", min_length=3, max_length=255)
