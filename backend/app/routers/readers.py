from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import models, schemas
from ..db import get_db

router = APIRouter(prefix="/readers", tags=["Readers"])

@router.get("/", response_model=list[schemas.ReaderOut])
def list_readers(db: Session = Depends(get_db)):
    """Retrieve a list of all readers."""
    readers = db.query(models.Reader).all()
    return readers

@router.post("/", response_model=schemas.ReaderOut, status_code=status.HTTP_201_CREATED)
def create_reader(reader: schemas.ReaderCreate, db: Session = Depends(get_db)):
    """Create a new reader."""
    db_reader = models.Reader(name=reader.name, email=reader.email)
    db.add(db_reader)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered.")
    db.refresh(db_reader)
    return db_reader

@router.get("/{reader_id}", response_model=schemas.ReaderOut)
def get_reader(reader_id: int, db: Session = Depends(get_db)):
    """Retrieve a reader by ID."""
    reader = db.query(models.Reader).filter(models.Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return reader

@router.put("/{reader_id}", response_model=schemas.ReaderOut)
def update_reader(reader_id: int, reader_update: schemas.ReaderUpdate, db: Session = Depends(get_db)):
    """Update an existing reader."""
    reader = db.query(models.Reader).filter(models.Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    
    if reader_update.name is not None:
        reader.name = reader_update.name
    if reader_update.email is not None:
        reader.email = reader_update.email
    
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered.")
    
    db.refresh(reader)
    return reader

@router.delete("/{reader_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reader(reader_id: int, db: Session = Depends(get_db)):
    """Delete a reader by ID."""
    reader = db.query(models.Reader).filter(models.Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    
    reader.books.clear()  # Remove all book associations
    db.delete(reader)
    db.commit()