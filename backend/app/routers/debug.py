from fastapi import APIRouter, Depends
from sqlalchemy import text, inspect
from sqlalchemy.orm import Session
from ..db import get_db, engine

router = APIRouter(prefix="/debug", tags=["Debug"])

@router.get("/db-ping", summary="Ping the database to check connectivity")
def db_ping(db: Session = Depends(get_db)):
    """Ping the database to check connectivity."""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "Database connection successful"}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}

@router.get("/db-tables", summary="List all tables in the database")
def list_db_tables():
    """List all tables in the database."""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return {"tables": tables}