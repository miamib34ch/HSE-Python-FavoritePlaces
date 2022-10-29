"""
Описание моделей данных (DTO).
"""
from typing import Optional

from pydantic import BaseModel, Field


class LocalityDTO(BaseModel):
    """
    Модель для представления данных о местонахождении.

    .. code-block::

        LocalityDTO(
            city="Mariehamn",
            alpha2code="AX",
            locality="Mariehamn sub-region",
        )
    """

    city: Optional[str] = Field(
        None, title="Название города", min_length=2, max_length=50
    )
    alpha2code: Optional[str] = Field(
        None, title="ISO Alpha2-код страны", min_length=2, max_length=2
    )
    locality: Optional[str] = Field(
        None, title="Местонахождение", min_length=2, max_length=255
    )
