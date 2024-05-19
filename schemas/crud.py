from .schemas import Content, Text

from typing import Optional, List
from sqlmodel import SQLModel, Session, create_engine

db_name = ''
db_user = ''
db_pass = ''

db_url = f'postgresql+psycopg2://{db_user}:{db_pass}@localhost:5432/{db_name}'

class ContentCrud():
    def __init__(self):
        self.engine = create_engine(db_url,echo=True)
        self.session = Session(self.engine)

    def add(self, content = Content) -> Content:
        new_record = Content(file_name=content.file_name,
                             is_nsfw=content.is_nsfw,
                             confidence_percentage=content.confidence_percentage,
                             content_type=content.content_type
                             )
        self.session.add(new_record)
        self.session.commit()
        return new_record