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
    description: str = Field(title="Описание", min_length=2, max_length=255)
    country: Optional[str] = Field(
        title="ISO Alpha2-код страны", min_length=2, max_length=2
    )
    city: Optional[str] = Field(title="Название города", min_length=2, max_length=50)
    locality: Optional[str] = Field(
        title="Местонахождение", min_length=2, max_length=255
    )
