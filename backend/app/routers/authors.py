from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..db import get_db

router = APIRouter(prefix="/authors", tags=["Authors"])

@router.get("/", response_model=list[schemas.AuthorOut])
def list_authors(db: Session = Depends(get_db)):
    """Retrieve a list of all authors."""
    authors = db.query(models.Author).all()
    return authors

@router.post("/", response_model=schemas.AuthorOut, status_code=201)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    """Create a new author."""
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

@router.get("/{author_id}", response_model=schemas.AuthorOut)
def get_author(author_id: int, db: Session = Depends(get_db)):
    """Retrieve an author by ID."""
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.put("/{author_id}", response_model=schemas.AuthorOut)
def update_author(author_id: int, author_update: schemas.AuthorUpdate, db: Session = Depends(get_db)):
    """Update an existing author."""
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    if author_update.name is not None:
        author.name = author_update.name
    if author_update.bio is not None:
        author.bio = author_update.bio
    
    db.commit()
    db.refresh(author)
    return author

@router.delete("/{author_id}", status_code=204)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    """Delete an author by ID."""
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    db.delete(author)
    db.commit()
