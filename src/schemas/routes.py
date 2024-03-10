from typing import Optional

from pydantic import BaseModel, Field


class MetadataTag(BaseModel):
    """Модель для описания метаданных для методов API."""

    name: str
    description: Optional[str] = None

    class Config:
        allow_population_by_field_name = True


class Description(BaseModel):
    """Модель для описания"""

    description: str = Field(None, min_length=3, max_length=255)
