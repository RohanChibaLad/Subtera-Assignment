from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2] # Gets the base directory of the project

DATABASE_URL = "sqlite:///BASE_DIR/database/library.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) #Makes sure its SQLite compatible

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #Creates a session factory

Base = declarative_base() #Base class for our models

def get_db():
    """Dependency to get DB session"""
    db = SessionLocal() #Creates a new session
    try:
        yield db #Yields the session to be used in the request
    finally:
        db.close() #Closes the session after the request is done