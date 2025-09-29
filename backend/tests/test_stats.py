from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

"""
stats.py has 4 endpoints:
1. GET /stats/popular-books - Get the most popular books based on the number of unique readers
2. GET /stats/popular-authors - Get the most popular authors based on the total number of unique readers across all their books
3. GET /stats/reader-stats/{reader_id} - Get statistics for a specific reader, including total books read and favorite author
4. GET /stats/user-top-authors - Get the top authors whose books have been read by the current user 

Tests:
1. test_get_popular_books: This test checks if the /stats/popular-books endpoint is working correctly by sending a GET request and verifying the response status code and content.
2. test_get_popular_authors: This test checks if the /stats/popular-authors endpoint is working correctly by sending a GET request and verifying the response status code and content.
3. test_get_user_total_books: This test checks if the /stats/user-total-books endpoint is working correctly by sending a GET request and verifying the response status code and content.
4. test_get_user_top_authors: This test checks if the /stats/user-top-auth
"""

def test_get_popular_books():
    response = client.get("/stats/popular-books")
    assert response.status_code == 200
    books = response.json()
    assert len(books) >= 5  # At least 5 popular books should be present
    
    book_titles = []
    for book in books:
        book_titles.append(book["title"])
    
    assert "Harry Potter and the Philosopher's Stone" in book_titles
    assert "The Hobbit" in book_titles
    assert "A Clash of Kings" in book_titles
    assert "A Game of Thrones" in book_titles
    assert "Death on the Nile" in book_titles
    
def test_get_popular_authors():
    response = client.get("/stats/popular-authors")
    assert response.status_code == 200
    authors = response.json()
    assert len(authors) >= 4  # At least 5 popular authors should be present
    
    author_names = []
    for author in authors:
        author_names.append(author["author_name"])
    
    assert "J.K. Rowling" in author_names
    assert "J.R.R. Tolkien" in author_names
    assert "George R.R. Martin" in author_names
    assert "Agatha Christie" in author_names

def test_get_user_total_books():
    response = client.get("/stats/user-total-books")
    assert response.status_code == 200
    user_stats = response.json()
    
    assert "reader_id" in user_stats
    assert "reader_name" in user_stats
    assert "total_books" in user_stats
    
    print(user_stats)
    assert user_stats["reader_name"] == "User One"
    assert user_stats["total_books"] == 4  # User One has read 4 books

def test_get_user_top_authors():
    response = client.get("/stats/user-top-authors")
    assert response.status_code == 200
    top_authors = response.json()
    assert len(top_authors) >= 3  # Top 3top authors should be present
    
    author_names = []
    for author in top_authors:
        author_names.append(author["author_name"])
    
    assert "J.K. Rowling" in author_names
    assert "Agatha Christie" in author_names
    assert "George R.R. Martin" in author_names
