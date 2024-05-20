from sqlmodel import SQLModel, create_engine
from schemas import Content, Text

db_name = 'valid'
db_user = 'postgres'
db_pass = 'admin'

db_url = f'postgresql+psycopg2://{db_user}:{db_pass}@db:5432/{db_name}'
engine = create_engine(db_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()
    print("Таблицы успешно созданы!")
