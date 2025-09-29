import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool


DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
     # Default to a local SQLite database file if DATABASE_URL is not set
    BASE_DIR = Path(__file__).resolve().parents[1] # Gets the base directory of the project
    DATABASE_DIR = BASE_DIR / "database" # Directory to store the database file
    DATABASE_DIR.mkdir(parents=True, exist_ok=True) # Create the directory if it doesn't exist
    DATABASE_URL = f"sqlite:///{DATABASE_DIR / 'app.db'}" # SQLite database URL

is_sqlite = DATABASE_URL.startswith("sqlite")
is_memory = DATABASE_URL in ("sqlite://", "sqlite:///:memory:")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if is_sqlite else {}, poolclass=StaticPool if is_memory else None,)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #Creates a session factory

Base = declarative_base() #Base class for our models

def get_db():
    """Dependency to get DB session"""
    db = SessionLocal() #Creates a new session
    try:
        yield db #Yields the session to be used in the request
    finally:
        db.close() #Closes the session after the request is done