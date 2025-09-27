from pydantic import BaseModel
from typing import Optional, List

# --- Author Schemas ---
class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None  
    
class AuthorCreate(AuthorBase):
    pass    

class AuthorUpdate(AuthorBase):
    name: Optional[str] = None
    bio: Optional[str] = None

class AuthorOut(AuthorBase):
    id: int
    
    class Config:
        from_attributes = True #Allows reading data from object attributes

# --- Book Schemas ---

class BookBase(BaseModel):
    title: str
    year_published: Optional[int] = None
    description: Optional[str] = None
    author_id: int

class BookCreate(BookBase):
    pass    

class BookUpdate(BookBase):
    title: Optional[str] = None
    year_published: Optional[int] = None
    description: Optional[str] = None
    author_id: Optional[int] = None

class BookOut(BookBase):
    id: int    

    class Config:
        from_attributes = True #Allows reading data from object attributes

# --- Reader Schemas ---

class ReaderBase(BaseModel):
    name: str
    email: str 

class ReaderCreate(ReaderBase):
    pass   

class ReaderUpdate(ReaderBase):
    name: Optional[str] = None
    email: Optional[str] = None
    
class ReaderOut(ReaderBase):
    id: int
    
    class Config:
        from_attributes = True #Allows reading data from object attributes
        
# --- Statistic Schemas ---

class PopularBookOut(BaseModel):
    book_id: int
    title: str
    author_id: int
    author_name: str
    readers_counter: int

class PopularAuthorOut(BaseModel):
    author_id: int
    author_name: str
    total_readers: int
    books: List[BookOut] = []

class UserTotalBooksOut(BaseModel):
    reader_id: int
    reader_name: str
    total_books: int

class UserTopAuthorsOut(BaseModel):
    reader_id: int
    reader_name: str
    author_id: int
    author_name: str
    books_read: int