from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase

from src.settings import Settings

DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(DATABASE_URL)


def get_session():
    with Session(engine) as session:  # pragma: nocover
        yield session