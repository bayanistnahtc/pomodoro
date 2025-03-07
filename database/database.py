from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from settings import Settings

setttings = Settings()
DB_URL = 'postgresql+psycopg2://postgres:password@localhost:5432/pomodoro'
engine = create_engine(DB_URL, echo=True)


def get_db_session() -> Session:
    return sessionmaker(engine)
