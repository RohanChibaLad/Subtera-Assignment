from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

"""
authors.py has 5 direct endpoints:
1. GET /authors - Retrieve a list of all authors.
2. POST /authors - Create a new author.
3. GET /authors/{author_id} - Retrieve an author by ID.
4. PUT /authors/{author_id} - Update an existing author.
5. DELETE /authors/{author_id} - Delete an author by ID.

Tests:
1. test_list_authors: This test checks if the /authors endpoint is working correctly by sending a GET request and verifying the response status code and content.
2. test_create_author: This test checks if a new author can be created by sending a POST request to the /authors endpoint and verifying the response status code and content.
3. test_get_author: This test checks if an author can be retrieved by ID by sending a GET request to the /authors/{author_id} endpoint and verifying the response status code and content.
4. test_update_author: This test checks if an existing author can be updated by sending a PUT request to the /authors/{author_id} endpoint and verifying the response status code and content.
5. test_delete_author: This test checks if an author can be deleted by sending a DELETE request to the /authors/{author_id} endpoint and verifying the response status code.
"""

def test_list_authors():
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
    
def test_create_author():
    new_author = {
        "name": "Test Author",
        "bio": "This is a test author."
    }
    response = client.post("/authors", json=new_author)
    assert response.status_code == 201
    created_author = response.json()
    assert created_author["name"] == new_author["name"]
    assert created_author["bio"] == new_author["bio"]
    assert "id" in created_author
    
def test_get_author():
    # First, create a new author to ensure it exists
    new_author = {
        "name": "Test Author 2",
        "bio": "This is another test author."
    }
    create_response = client.post("/authors", json=new_author)
    assert create_response.status_code == 201
    created_author = create_response.json()
    author_id = created_author["id"]
    
    # Now, retrieve the author by ID
    get_response = client.get(f"/authors/{author_id}")
    assert get_response.status_code == 200
    retrieved_author = get_response.json()
    assert retrieved_author["name"] == new_author["name"]
    assert retrieved_author["bio"] == new_author["bio"]
    assert retrieved_author["id"] == author_id
    
def test_update_author():
    # First, create a new author to ensure it exists
    new_author = {
        "name": "Test Author 3",
        "bio": "This is yet another test author."
    }
    create_response = client.post("/authors", json=new_author)
    assert create_response.status_code == 201
    created_author = create_response.json()
    author_id = created_author["id"]
    
    # Now, update the author's details
    updated_author = {
        "name": "Updated Test Author 3",
        "bio": "This is an updated test author."
    }
    update_response = client.put(f"/authors/{author_id}", json=updated_author)
    assert update_response.status_code == 200
    updated_author_response = update_response.json()
    assert updated_author_response["name"] == updated_author["name"]
    assert updated_author_response["bio"] == updated_author["bio"]
    assert updated_author_response["id"] == author_id

def test_delete_author():
    # First, create a new author to ensure it exists
    new_author = {
        "name": "Test Author 4",
        "bio": "This is a test author to be deleted."
    }
    create_response = client.post("/authors", json=new_author)
    assert create_response.status_code == 201
    created_author = create_response.json()
    author_id = created_author["id"]
    
    # Now, delete the author
    delete_response = client.delete(f"/authors/{author_id}")
    assert delete_response.status_code == 204
    
    # Verify the author has been deleted
    get_response = client.get(f"/authors/{author_id}")
    assert get_response.status_code == 404
    
