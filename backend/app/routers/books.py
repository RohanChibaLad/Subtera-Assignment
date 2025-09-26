from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import models, schemas
from ..db import get_db

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=list[schemas.BookOut])
def list_books(
    author_id: int | None = Query(None, description="Filter books by author ID"),
    year_published: int | None = Query(None, description="Filter books by year published"),
    db: Session = Depends(get_db)):
    
    """Retrieve a list of all books, with optional filters for author and year published."""
    query = db.query(models.Book)
    
    if author_id is not None:
        query = query.filter(models.Book.author_id == author_id)
    if year_published is not None:
        query = query.filter(models.Book.year_published == year_published)
    
    books = query.all()
    return books

@router.post("/", response_model=schemas.BookOut, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Create a new book."""
    db_book = models.Book(
        title=book.title,
        year_published=book.year_published,
        description=book.description,
        author_id=book.author_id
    )
    db.add(db_book)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Author with given ID does not exist.")
    db.refresh(db_book)
    return db_book

@router.get("/{book_id}", response_model=schemas.BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Retrieve a book by ID."""
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=schemas.BookOut)
def update_book(book_id: int, book_update: schemas.BookUpdate, db: Session = Depends(get_db)):
    """Update an existing book."""
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if book_update.title is not None:
        book.title = book_update.title
    if book_update.year_published is not None:
        book.year_published = book_update.year_published
    if book_update.description is not None:
        book.description = book_update.description
    if book_update.author_id is not None:
        book.author_id = book_update.author_id
    
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Author with given ID does not exist.")
    
    db.refresh(book)
    return book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete a book by ID."""
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(book)
    db.commit()