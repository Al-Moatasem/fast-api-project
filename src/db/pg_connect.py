from sqlalchemy import create_engine

# declarative_base on SqlAlchemy 1.4, deprecated
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker

from src.configs.config import settings

PG_CONNECTION_URL = settings.pg_connection_url


engine_echo = True if settings.debug else False

engine = create_engine(PG_CONNECTION_URL, echo=engine_echo)

SessionFactory = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


# Creating a database session through SQLAlchemy
def db_session():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
        return engine
