from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

"""
main.py has 2 direct enpoints:
1. GET /health - A health check endpoint to verify if the API is running.
2. on_startup - An event that initializes the database and inserts the seed data into the database when the application starts

Tests:
1. test_health_check: This test checks if the /health endpoint is working correctly by sending a GET request and verifying the response status code and content.
2. test_databases_connected: This test checks if the database connection is established correctly by sending a GET request to the /database/db-ping endpoint and verifying the response status code.
3. test_databases_tables: This test checks if the database tables are created correctly by sending a GET request to the /database/db-tables endpoint and verifying the response status code and content.
4. test_readers_seed_data: This test checks if the seed data for readers has been correctly inserted into the database by sending a GET request to the /readers endpoint and verifying the response content.
5. test_authors_seed_data: This test checks if the seed data for authors has been correctly inserted into the database by sending a GET request to the /authors endpoint and verifying the response content.
6. test_books_seed_data: This test checks if the seed data for books has been correctly inserted into the database by sending a GET request to the /books endpoint and verifying the response content.
"""

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_databases_connected():
    response = client.get("/database/db-ping")
    assert response.status_code == 200
    assert response.json().get("status") == "Database connection successful"

def test_databases_tables():
    response = client.get("/database/db-tables")
    assert response.status_code == 200
    tables = response.json().get("tables", [])
    expected_tables = ["authors", "books", "readers", "readers_books"]
    for table in expected_tables:
        assert table in tables
        
def test_readers_seed_data():
    response = client.get("/readers")
    assert response.status_code == 200
    readers = response.json()
    assert len(readers) >= 5  # At least 5 readers should be present
    
    reader_names = []
    for reader in readers:
        reader_names.append(reader["name"])
    
    assert "User One" in reader_names
    assert "User Two" in reader_names
    assert "User Three" in reader_names
    assert "User Four" in reader_names
    assert "User Five" in reader_names
    
def test_authors_seed_data():
    response = client.get("/authors")
    assert response.status_code == 200
    authors = response.json()
    assert len(authors) >= 4  # At least 4 authors should be present
    
    author_names = []
    for author in authors:
        author_names.append(author["name"])
        
    assert "J.K. Rowling" in author_names
    assert "George R.R. Martin" in author_names
    assert "J.R.R. Tolkien" in author_names
    assert "Agatha Christie" in author_names

def test_books_seed_data():
    response = client.get("/books")
    assert response.status_code == 200
    books = response.json()
    assert len(books) >= 16  # At least 16 books should be present
    book_titles = []
    for book in books:
        book_titles.append(book["title"])
        
    assert "Harry Potter and the Philosopher's Stone" in book_titles
    assert "Harry Potter and the Chamber of Secrets" in book_titles
    assert "Harry Potter and the Prisoner of Azkaban" in book_titles
    assert "Harry Potter and the Goblet of Fire" in book_titles
    
    assert "A Game of Thrones" in book_titles
    assert "A Clash of Kings" in book_titles
    assert "A Storm of Swords" in book_titles
    assert "A Feast for Crows" in book_titles
    
    assert "The Hobbit" in book_titles
    assert "The Fellowship of the Ring" in book_titles
    assert "The Two Towers" in book_titles
    assert "The Return of the King" in book_titles
    
    assert "Murder on the Orient Express" in book_titles
    assert "Death on the Nile" in book_titles
    assert "A Holiday for Murder" in book_titles
    assert "Murder after Hours" in book_titles