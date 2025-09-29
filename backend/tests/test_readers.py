from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

"""
readers.py has 5 endpoints:
1. GET /readers/ - List all readers
2. POST /readers/ - Create a new reader
3. GET /readers/{reader_id} - Get a reader by ID
4. PUT /readers/{reader_id} - Update a reader by ID
5. DELETE /readers/{reader_id} - Delete a reader by ID

Tests:
1. test_list_readers: This test checks if the /readers/ endpoint is working correctly by sending a GET request and verifying the response status code and content.
2. test_create_reader: This test checks if a new reader can be created by sending a POST request to the /readers/ endpoint and verifying the response status code and content.
3. test_create_reader_duplicate_email: This test checks if the API correctly handles the case when an attempt is made to create a reader with an email that already exists by sending a POST request with a duplicate email and verifying the response status code and error message.
4. test_get_reader: This test checks if a reader can be retrieved by ID by sending a GET request to the /readers/{reader_id} endpoint and verifying the response status code and content.
5. test_get_reader_not_found: This test checks if the API correctly handles the case when an attempt is made to retrieve a non-existent reader by sending a GET request with an invalid ID and verifying the response status code and error message.
6. test_update_reader: This test checks if an existing reader can be updated by sending a PUT request to the /readers/{reader_id} endpoint and verifying the response status code and content.
7. test_update_reader_not_found: This test checks if the API correctly handles the case when an attempt is made to update a non-existent reader by sending a PUT request with an invalid ID and verifying the response status code and error message.
8. test_update_reader_duplicate_email: This test checks if the API correctly handles the case when an attempt is made to update a reader with an email that already exists by sending a PUT request with a duplicate email and verifying the response status code and error message.
9. test_delete_reader: This test checks if a reader can be deleted by sending a DELETE request to the /readers/{reader_id} endpoint and verifying the response status code.
10. test_delete_reader_not_found: This test checks if the API correctly handles the case when an attempt is made to delete a non-existent reader by sending a DELETE request with an invalid ID and verifying the response status code and error message.
"""

def test_list_readers():
    response = client.get("/readers/")
    assert response.status_code == 200
    readers = response.json()
    assert len(readers) >= 5  # At least 3 readers should be present
    
    reader_names = []
    for reader in readers:
        reader_names.append(reader["name"])
    
    assert "User One" in reader_names
    assert "User Two" in reader_names
    assert "User Three" in reader_names
    assert "User Four" in reader_names
    assert "User Five" in reader_names

def test_create_reader():
    new_reader = {
        "name": "New User",
        "email": "newuser@gmai.com"
    }
    response = client.post("/readers/", json=new_reader)
    assert response.status_code == 201
    created_reader = response.json()
    assert created_reader["name"] == new_reader["name"]
    assert created_reader["email"] == new_reader["email"]

def test_create_reader_duplicate_email():
    new_reader = {
        "name": "New User",
        "email": "newuser@gmail.com"
    }
    duplicate_reader = {
        "name": "Another User",
        "email": "newuser@gmail.com"
    }
    response = client.post("/readers/", json=new_reader)
    assert response.status_code == 201
    response = client.post("/readers/", json=duplicate_reader)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered."
    
def test_get_reader():
    response = client.get("/readers/")
    assert response.status_code == 200
    readers = response.json()
    reader_id = readers[0]["id"]
    
    response = client.get(f"/readers/{reader_id}")
    assert response.status_code == 200
    reader = response.json()
    assert reader["id"] == reader_id

def test_get_reader_not_found():
    response = client.get("/readers/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Reader not found"

def test_update_reader():
    response = client.get("/readers/")
    assert response.status_code == 200
    readers = response.json()
    reader_id = readers[0]["id"]
    
    update_data = {
        "name": "Updated User",
        "email": "newemail@gmail.com"
    }
    response = client.put(f"/readers/{reader_id}", json=update_data)
    assert response.status_code == 200
    updated_reader = response.json()
    assert updated_reader["name"] == update_data["name"]
    assert updated_reader["email"] == update_data["email"]

def test_update_reader_not_found():
    update_data = {
        "name": "Updated User",
        "email": "newemail@gmail.com"
    }
    response = client.put("/readers/9999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Reader not found" 

def test_update_reader_duplicate_email():
    response = client.get("/readers/")
    assert response.status_code == 200
    readers = response.json()
    reader_id_1 = readers[0]["id"]
    reader_2_email = readers[1]["email"]
    
    update_data = {
        "email": reader_2_email  # Trying to update to an email that already exists
    }
    response = client.put(f"/readers/{reader_id_1}", json=update_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered." 

def test_delete_reader():
    response = client.get("/readers/")
    assert response.status_code == 200
    readers = response.json()
    reader_id = readers[0]["id"]
    
    response = client.delete(f"/readers/{reader_id}")
    assert response.status_code == 204
    
    # Verify deletion
    response = client.get(f"/readers/{reader_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Reader not found"

def test_delete_reader_not_found():
    response = client.delete("/readers/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Reader not found"

