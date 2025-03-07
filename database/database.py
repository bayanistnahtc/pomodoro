from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from settings import Settings

setttings = Settings()
engine = create_engine(setttings.db_url, echo=True)


def get_db_session() -> Session:
    return sessionmaker(engine)
