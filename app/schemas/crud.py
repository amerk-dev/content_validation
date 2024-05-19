# crud.py
from typing import List, Optional
from sqlmodel import SQLModel, Session, create_engine, select
from .schemas import Content, Text

db_name = 'valid'
db_user = 'postgres'
db_pass = 'admin'

db_url = f'postgresql+psycopg2://{db_user}:{db_pass}@localhost:5432/{db_name}'


class ContentCrud:
    def __init__(self):
        self.engine = create_engine(db_url, echo=True)

    def add(self, content: Content) -> Content:
        with Session(self.engine) as session:
            session.add(content)
            session.commit()
            session.refresh(content)
            return content

    def get(self, content_id: int) -> Optional[Content]:
        with Session(self.engine) as session:
            statement = select(Content).where(Content.id == content_id)
            result = session.exec(statement)
            return result.first()

    def get_all(self) -> List[Content]:
        with Session(self.engine) as session:
            statement = select(Content)
            result = session.exec(statement)
            return result.all()

    def update(self, content_id: int, content_data: dict) -> Optional[Content]:
        with Session(self.engine) as session:
            content = session.get(Content, content_id)
            if not content:
                return None
            for key, value in content_data.items():
                setattr(content, key, value)
            session.add(content)
            session.commit()
            session.refresh(content)
            return content

    def delete(self, content_id: int) -> bool:
        with Session(self.engine) as session:
            content = session.get(Content, content_id)
            if not content:
                return False
            session.delete(content)
            session.commit()
            return True


class TextCrud:
    def __init__(self):
        self.engine = create_engine(db_url, echo=True)

    def add(self, text: Text) -> Text:
        with Session(self.engine) as session:
            session.add(text)
            session.commit()
            session.refresh(text)
            return text

    def get(self, text_id: int) -> Optional[Text]:
        with Session(self.engine) as session:
            statement = select(Text).where(Text.id == text_id)
            result = session.exec(statement)
            return result.first()

    def get_all(self) -> List[Text]:
        with Session(self.engine) as session:
            statement = select(Text)
            result = session.exec(statement)
            return result.all()

    def update(self, text_id: int, text_data: dict) -> Optional[Text]:
        with Session(self.engine) as session:
            text = session.get(Text, text_id)
            if not text:
                return None
            for key, value in text_data.items():
                setattr(text, key, value)
            session.add(text)
            session.commit()
            session.refresh(text)
            return text

    def delete(self, text_id: int) -> bool:
        with Session(self.engine) as session:
            text = session.get(Text, text_id)
            if not text:
                return False
            session.delete(text)
            session.commit()
            return True
