from fastapi import FastAPI

from transport.handlers import places
from transport.handlers.places import tag_places

metadata_tags = [tag_places]


def setup_routes(app: FastAPI) -> None:
    """Настройка маршрутов для API"""

    app.include_router(
        places.router,
        prefix="/api/v1/places",
        tags=[tag_places.name],
    )
