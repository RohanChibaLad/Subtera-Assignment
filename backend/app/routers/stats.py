from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from ..db import get_db
from .. import models, schemas

router = APIRouter(prefix="/stats", tags=["Statistics"])

def get_current_reader(db: Session) -> models.Reader:
    """Fetch the current reader. For the task, we return the first reader."""
    
    return db.query(models.Reader).first()

@router.get("/popular-books", response_model=list[schemas.PopularBookOut])
def get_popular_books(limit: int = Query(10, description="Number of top popular books to retrieve"), db: Session = Depends(get_db)):
    """Retrieve the most popular books based on the number of unique readers."""
    
    rb = models.readers_books

    
    subquery = (
            db.query(
                    models.Book.id.label("book_id"),
                    models.Book.title.label("title"),
                    models.Book.author_id.label("author_id"),
                    models.Author.name.label("author_name"),
                    func.count(func.distinct(rb.reader_id)).label("readers_counter")
                )
                .join(rb, models.Book.id == rb.book_id)
                .join(models.Author, models.Book.author_id == models.Author.id)
                .group_by(models.Book.id, models.Author.id)
                .subquery())
    
    results = (db.query(subquery)
               .order_by(desc(subquery.c.readers_counter))
               .limit(limit)
               .all())
    
    return results

@router.get("/popular-authors", response_model=list[schemas.PopularAuthorOut])
def get_popular_authors(limit: int = Query(10, description="Number of top popular authors to retrieve"), db: Session = Depends(get_db)):
    """Retrieve the most popular authors based on the total number of unique readers across all their books."""
    
    rb = models.readers_books

    subquery = (
            db.query(
                    models.Author.id.label("author_id"),
                    models.Author.name.label("author_name"),
                    func.count(func.distinct(rb.c.reader_id)).label("total_readers")
                )
                #Table joins for author-reader relationship
                .join(models.Book, models.Author.id == models.Book.author_id)
                .outerjoin(rb, models.Book.id == rb.c.book_id)
                .group_by(models.Author.id)
                .order_by(desc("total_readers"), models.Author.name.asc())
                .limit(limit)
    )
    
    rows = subquery.all()
    
    results: list[schemas.PopularAuthorOut] = []
    for row in rows:
        results.append(
            schemas.PopularAuthorOut.model_validate(row._mapping))
    
    return results
    
    
@router.get("/user-total-books", response_model=list[schemas.UserTotalBooksOut])
def get_user_total_books(db: Session = Depends(get_db)):
    """Retrieve the total number of books read by each user."""
    
    user = get_current_reader(db)
    if not user:
        return schemas.UserTotalBooksOut(reader_id=0,, reader_name="" total_books=0)
    
    rb = models.readers_books
    
    total = db.query(func.count(rb.c.book_id)).filter(rb.c.reader_id == user.id).scalar()
    
    return [schemas.UserTotalBooksOut(reader_id=user.id, reader_name=user.name, total_books=total)]