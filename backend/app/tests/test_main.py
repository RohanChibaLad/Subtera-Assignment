from fastapi.testclient import TestClient
from ..main import app

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