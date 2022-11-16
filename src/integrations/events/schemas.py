from pydantic import BaseModel, Field


class CountryCityDTO(BaseModel):
    """
    Модель данных для идентификации города.
    Содержит ISO Alpha2-код страны и название города.

    .. code-block::

        CountryCityDTO(
            city="Mariehamn",
            alpha2code="AX",
        )
    """

    city: str
    alpha2code: str = Field(min_length=2, max_length=2)
