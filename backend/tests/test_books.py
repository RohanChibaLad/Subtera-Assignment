from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

""" 
books.py has 5 direct endpoints:
1. GET /books - Retrieve a list of all books, with optional filters for author and year published.
2. POST /books - Create a new book.
3. GET /books/{book_id} - Retrieve a book by ID.
4. PUT /books/{book_id} - Update an existing book.
5. DELETE /books/{book_id} - Delete a book by ID.

Tests:
1. test_list_books: This test checks if the /books endpoint is working correctly by sending a GET request and verifying the response status code and content.
2. test_create_book: This test checks if a new book can be created by sending a POST request to the /books endpoint and verifying the response status code and content.
3. test_create_book_no_title: This test checks if the API correctly handles the case when an attempt is made to create a book without a title by sending a POST request with an empty title and verifying the response status code and error message.
4. test_create_book_invalid_author: This test checks if the API correctly handles the case when an attempt is made to create a book with a non-existent author ID by sending a POST request with an invalid author_id and verifying the response status code and error message.
5. test_get_book: This test checks if a book can be retrieved by ID by sending a GET request to the /books/{book_id} endpoint and verifying the response status code and content.
6. test_get_book_not_found: This test checks if the API correctly handles the case when an attempt is made to retrieve a non-existent book by sending a GET request with an invalid ID and verifying the response status code and error message.
7. test_update_book: This test checks if an existing book can be updated by sending a PUT request to the /books/{book_id} endpoint and verifying the response status code and content.
8. test_update_book_not_found: This test checks if the API correctly handles the case when an attempt is made to update a non-existent book by sending a PUT request with an invalid ID and verifying the response status code and error message.
9. test_update_book_no_title: This test checks if the API correctly handles the case when an attempt is made to update a book without a title by sending a PUT request with an empty title and verifying the response status code and error message.
10. test_update_book_invalid_author: This test checks if the API correctly handles the case when an attempt is made to update a book with a non-existent author ID by sending a PUT request with an invalid author_id and verifying the response status code and error message.
11. test_delete_book: This test checks if a book can be deleted by sending a DELETE request to the /books/{book_id} endpoint and verifying the response status code.
12. test_delete_book_not_found: This test checks if the API correctly handles the case when an attempt is made to delete a non-existent book by sending a DELETE request with an invalid ID

"""

def test_list_books():
    response = client.get("/books")
    assert response.status_code == 200
    books = response.json()
    assert len(books) >= 4  # At least 4 books should be present
    
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

def test_create_book():
    new_book = {
        "title": "Test Book",
        "year_published": 2023,
        "description": "A book created during testing.",
        "author_id": 1  # Assuming author with ID 1 exists
    }
    response = client.post("/books", json=new_book)
    assert response.status_code == 201
    book = response.json()
    assert book["title"] == new_book["title"]
    assert book["year_published"] == new_book["year_published"]
    assert book["description"] == new_book["description"]
    assert book["author_id"] == new_book["author_id"]

def test_create_book_no_title():
    new_book = {
        "title": "   ",  # Title with only spaces
        "year_published": 2023,
        "description": "A book without a title.",
        "author_id": 1  # Assuming author with ID 1 exists
    }
    response = client.post("/books", json=new_book)
    assert response.status_code == 400
    assert response.json()["detail"] == "Book title cannot be empty"

def test_create_book_invalid_author():
    new_book = {
        "title": "Test Book with Invalid Author",
        "year_published": 2023,
        "description": "A book with a non-existent author.",
        "author_id": 9999  # Assuming this author ID does not exist
    }
    response = client.post("/books", json=new_book)
    assert response.status_code == 400
    assert response.json()["detail"] == "Author with given ID does not exist."
    
def test_get_book():
    response = client.get("/books/1")  # Assuming book with ID 1 exists
    assert response.status_code == 200
    book = response.json()
    assert book["id"] == 1
    
def test_get_book_not_found():
    response = client.get("/books/9999")  # Assuming this book ID does not exist
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"   
    
def test_update_book():
    update_data = {
        "title": "Updated Test Book",
        "year_published": 2024,
        "description": "An updated description.",
        "author_id": 1  # Assuming author with ID 1 exists
    }
    response = client.put("/books/1", json=update_data)  # Assuming book with ID 1 exists
    assert response.status_code == 200
    book = response.json()
    assert book["title"] == update_data["title"]
    assert book["year_published"] == update_data["year_published"]
    assert book["description"] == update_data["description"]
    assert book["author_id"] == update_data["author_id"]

def test_update_book_not_found():
    update_data = {
        "title": "Non-existent Book",
        "year_published": 2024,
        "description": "Trying to update a non-existent book.",
        "author_id": 1  # Assuming author with ID 1 exists
    }
    response = client.put("/books/9999", json=update_data)  # Assuming this book ID does not exist
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

def test_update_book_no_title():
    update_data = {
        "title": "   ",  # Title with only spaces
        "year_published": 2024,
        "description": "Trying to update book without a title.",
        "author_id": 1  # Assuming author with ID 1 exists
    }
    response = client.put("/books/1", json=update_data)  # Assuming book with ID 1 exists
    assert response.status_code == 400
    assert response.json()["detail"] == "Book title cannot be empty"

def test_update_book_invalid_author():
    update_data = {
        "title": "Test Book with Invalid Author Update",
        "year_published": 2024,
        "description": "Trying to update book with a non-existent author.",
        "author_id": 9999  # Assuming this author ID does not exist
    }
    response = client.put("/books/1", json=update_data)  # Assuming book with ID 1 exists
    assert response.status_code == 400
    assert response.json()["detail"] == "Author with given ID does not exist."

def test_delete_book():
    response = client.delete("/books/1")  # Assuming book with ID 1 exists
    assert response.status_code == 204

def test_delete_book_not_found():
    response = client.delete("/books/9999")  # Assuming this book ID does not exist
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"
