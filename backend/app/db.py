from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1] # Gets the base directory of the project
DATABASE_DIR = BASE_DIR / "database" # Directory to store the database file
DATABASE_DIR.mkdir(parents=True, exist_ok=True) # Create the directory if it doesn't exist
DATABASE_URL = f"sqlite:///{DATABASE_DIR / 'app.db'}" # SQLite database URL

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