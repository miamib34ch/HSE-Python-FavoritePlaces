from pydantic import BaseModel


class ListResponse(BaseModel):
    """
    Схема для представления данных в виде списка.
    """

    data: list
