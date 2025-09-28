import os, sys, pytest
from pathlib import Path

# Make 'app' importable and configure test DB BEFORE importing app
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

os.environ["DATABASE_URL"] = "sqlite://"    # in-memory DB per run
os.environ["SKIP_STARTUP_SEED"] = "1"       # seed outselves

from app.main import app
from app.db import Base, engine, SessionLocal, get_db
from app import seed
from fastapi.testclient import TestClient

def override_get_db():
    with SessionLocal() as db:
        yield db

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True, scope="function")
def fresh_db():
    """Fresh schema + seed before every test (or change to scope='session' to seed once)."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed.seed_database(db)  # idempotent + commits
    yield

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
