from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .db import Base

readers_books = Table(
    'readers_books',
    Base.metadata,
    Column('reader_id', Integer, ForeignKey('readers.id'), primary_key=True),
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True)
)

class Author(Base):
    """Author model representing authors in the database."""
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    bio = Column(String, nullable=True)
    
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")
    
class Book(Base):
    """Book model representing books in the database."""
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    year_published = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    
    author = relationship("Author", back_populates="books")
    readers = relationship("Reader", secondary=readers_books, back_populates="books")

class Reader(Base):
    """Reader model representing readers in the database."""
    __tablename__ = 'readers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    
    books = relationship("Book", secondary=readers_books, back_populates="readers")