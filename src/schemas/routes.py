from typing import Optional

from pydantic import BaseModel


class MetadataTag(BaseModel):
    """Модель для описания метаданных для методов API."""

    name: str
    description: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
