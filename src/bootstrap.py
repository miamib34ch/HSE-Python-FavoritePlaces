from fastapi import FastAPI

from exceptions import setup_exception_handlers
from routes import metadata_tags, setup_routes
from settings import settings


def build_app() -> FastAPI:
    """Создание приложения FastAPI."""

    app_params = {
        "debug": settings.debug,
        "openapi_tags": metadata_tags,
        "title": f'API системы "{settings.project.title}"',
        "description": settings.project.description,
        "version": settings.project.release_version,
    }
    app = FastAPI(**app_params)

    setup_routes(app)
    setup_exception_handlers(app)

    return app
