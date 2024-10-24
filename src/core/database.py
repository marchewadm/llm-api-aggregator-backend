from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .config import settings


engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator:
    """
    Get a database connection.

    This function is a generator that manages the database session.
    It initializes a session before performing operations on the database and
    ensures that the session is closed after the operations are completed,
    regardless of whether the operations succeed or fail.

    Yields:
        Session: A database connection session object.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
