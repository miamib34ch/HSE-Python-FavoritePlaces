from typing import Type

from models import Place
from repositories.base_repository import BaseRepository


class PlacesRepository(BaseRepository):
    """
    Репозиторий для списка любимых мест.
    """

    @property
    def model(self) -> Type[Place]:
        return Place
