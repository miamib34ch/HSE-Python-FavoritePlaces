from pydantic import BaseModel, BaseSettings, Field, PostgresDsn


class Project(BaseModel):
    """
    Описание проекта.
    """

    #: название проекта
    title: str = "Favorite Places Service"
    #: описание проекта
    description: str = "Сервис для сохранения любимых мест."
    #: версия релиза
    release_version: str = Field(default="0.1.0")


class Settings(BaseSettings):
    """
    Настройки проекта.
    """

    #: режим отладки
    debug: bool = Field(default=False)
    #: описание проекта
    project: Project = Project()
    #: базовый адрес приложения
    base_url: str = Field(default="http://0.0.0.0:8000")
    #: строка подключения к БД
    database_url: PostgresDsn = Field(
        default="postgresql+asyncpg://favorite_places_user:secret@db/favorite_places"
    )

    class Config:
        env_file = ".env"


# инициализация настроек приложения
settings = Settings()
