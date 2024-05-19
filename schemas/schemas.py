from typing import Optional,List
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship, create_engine


# class PhotoResponse(SQLModel, table=True):
#     id: Optional[int] | Field(default=None, primary_key=True)
#     file_name: str
#     is_nsfw: Optional[bool] | Field(default=False)
#     confidence_percentage: float
#
#
# class VideoResponse(SQLModel, table=True):
#     id: Optional[int] | Field(default=None, primary_key=True)
#     file_name: str
#     is_nsfw: Optional[bool] | Field(default=False)
#     confidence_percentage: float

class ContentType(Enum):
    video = 'video'
    photo = 'photo'

class Content(SQLModel, table=True):
    id: Optional[int] | Field(default=None, primary_key=True)
    file_name: str
    is_nsfw: Optional[bool] | Field(default=False)
    confidence_percentage: float
    content_type: Optional[ContentType]

class Text(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    valid: bool

class TextResponse(SQLModel):
    valid: Optional[bool]


# db_name = "webstr"
# db_url = f"postgresql://postgres:admin@localhost:5432/{db_name}"
#
# engine = create_engine(db_url, echo=True)
#
# SQLModel.metadata.create_all(engine)