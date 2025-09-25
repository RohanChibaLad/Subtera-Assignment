from sqlalchemy.orm import Session
from . import models

def seed_database(db: Session):
    """Seed the database with initial data."""
    if db.query(models.Author).first():
        return  # Database already seeded  
    
    # Create authors
    authors = [
        models.Author(name="J.K. Rowling", bio="British author, best known for the Harry Potter series."),
        models.Author(name="George R.R. Martin", bio="American novelist and short story writer, known for A Song of Ice and Fire."),
        models.Author(name="J.R.R. Tolkien", bio="English writer, poet, and academic, author of The Lord of the Rings."),
        models.Author(name="Agatha Christie", bio="English writer known for her sixty-six detective novels and fourteen short story collections.")
    ]
    
    db.add_all(authors)
    db.flush() 
    
    #Add books
    books = [
        models.Book(title="Harry Potter and the Philosopher's Stone", year_published=1997, description="The first book in the Harry Potter series.", author_id=authors[0].id),
        models.Book(title="Harry Potter and the Chamber of Secrets", year_published=1998, description="The second book in the Harry Potter series.", author_id=authors[0].id),
        models.Book(title="Harry Potter and the Prisoner of Azkaban", year_published=1999, description="The third book in the Harry Potter series.", author_id=authors[0].id),
        models.Book(title="Harry Potter and the Goblet of Fire", year_published=2000, description="The fourth book in the Harry Potter series.", author_id=authors[0].id),
        
        models.Book(title="A Game of Thrones", year_published=1996, description="The first book in A Song of Ice and Fire series.", author_id=authors[1].id),
        models.Book(title="A Clash of Kings", year_published=1998, description="The second book in A Song of Ice and Fire series.", author_id=authors[1].id),
        models.Book(title="A Storm of Swords", year_published=2000, description="The third book in A Song of Ice and Fire series.", author_id=authors[1].id),
        models.Book(title="A Feast for Crows", year_published=2005, description="The fourth book in A Song of Ice and Fire series.", author_id=authors[1].id),
        
        models.Book(title="The Hobbit", year_published=1937, description="A fantasy novel and children's book by J.R.R. Tolkien.", author_id=authors[2].id),
        models.Book(title="The Fellowship of the Ring", year_published=1954, description="The first volume of The Lord of the Rings.", author_id=authors[2].id),
        models.Book(title="The Two Towers", year_published=1954, description="The second volume of The Lord of the Rings.", author_id=authors[2].id),
        models.Book(title="The Return of the King", year_published=1955, description="The third volume of The Lord of the Rings.", author_id=authors[2].id),
        
        models.Book(title="Murder on the Orient Express", year_published=1934, description="A detective novel featuring Hercule Poirot aboard the Orient Express.", author_id=authors[3].id),
        models.Book(title="Death on the Nile", year_published=1937, description="A detective novel featuring Hercule Poirot along the River Nile.", author_id=authors[3].id),
        models.Book(title="A Holiday for Murder", year_published=1938, description="A detective novel featuring Hercule Poirot on Christmas Eve.", author_id=authors[3].id),
        models.Book(title="Murder after Hours", year_published=1946, description="A detective novel featuring Hercule Poirot investigating a death in a swimming pool.", author_id=authors[3].id)
    ]
    
    db.add_all(books)
    db.flush()
    
    #Add Readers
    readers = [
        models.Reader(name="User One", email="userone@gmail.com"),
        models.Reader(name="User Two", email="usertwo@gmail.com"),
        models.Reader(name="User Three", email="userthree@gmail.com"),
        models.Reader(name="User Four", email="userfour@gmail.com"),
        models.Reader(name="User Five", email="userfive@gmail.com"),
    ]
    
    db.add_all(readers)
    db.flush()
    
    #reader_books Relationships
    #Books
    hp1 = books[0]
    hp2 = books[1]
    hp3 = books[2]
    hp4 = books[3]
    
    got1 = books[4]
    got2 = books[5]
    got3 = books[6]
    got4 = books[7]
    
    h = books[8]
    lotr1 = books[9]
    lotr2 = books[10]
    lotr3 = books[11]
    
    orient = books[12]
    nile = books[13]
    holiday = books[14]
    pool = books[15]
    
    #Readers
    user1 = readers[0]
    user2 = readers[1]
    user3 = readers[2]
    user4 = readers[3]
    user5 = readers[4]
    
    user1.books = [hp1, got1, h, orient]
    user2.books = [hp2, got2, lotr1, nile, pool, hp4]
    user3.books = [hp3, got3, lotr2, holiday, hp1]
    user4.books = [hp4, got4, lotr3, pool, h]
    user5.books = [hp1, hp2, got1, got2, h, lotr1, orient, nile]
    
    db.commit()