from typing import Optional
from enum import Enum
from sqlmodel import Field, SQLModel, create_engine

class ContentType(str, Enum):  # Используйте str для совместимости с Pydantic/SQLModel
    video = 'video'
    photo = 'photo'

class Content(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    file_name: str
    is_nsfw: Optional[bool] = Field(default=False)
    confidence_percentage: float
    content_type: Optional[ContentType]

    class Config:
        arbitrary_types_allowed = True  # Разрешить произвольные типы

class Text(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    valid: bool
