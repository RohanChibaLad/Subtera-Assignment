**Subtera Library - Mini Project Assessment**

A small library system with a FastAPI backend and a React frontend. It exposes CRUD for Authors/Books/Readers and a small dashboard with statistics.

**Key Features:**
1. FastAPI + SQLAlchemy + SQLite
2. Auto DB migrations and seeds data on startup
3. Fully tested backend with pytest
4. Clean and simple Vite react frontend
5. Docker compose for a one command run

**Project Structure**

**Backend:** 
1. backend/app - Contains all of the core fastAPI app files 
2. backend/routers - Contains all of the endpoints for the backend app (CRUD operation endpoinds, database seeding and statistic endpoinds)
3. backend/app/test - Contains all of the pytest tests
4. backend/requirements.txt - Contains the requirements for the backend of this project


**Frontend:**
1. frontend/src - Contains the main react files
2. frontend/src/pages/javascript - Contains all of the pages files
3. frontend/src/css - Contains all of the css files for styling


**Running the App**

**Option A: Using Docker:**
1. From the root folder (Subtera-Assignment), run docker compose up --build
2. Wait for the images to be built


**Option B: Individual Terminals:**
1. Open up a termninal in the root folder and make a virtual environment and activate it
2. Install the requiremetns located in the backend folder (pip install -r requirements.txt)
3. cd back into the root directory and run: uvicorn app.main:app --reload --app-dir backend
4. The backend should now be running
5. Open up another terminal and cd into the frontend folder
6. Run: npm ci
7. Then run npm run dev

Once option A or B have been followed, proceed to http://localhost:5173/


**API Overview**
**Authors**
1. GET /authors — list
2. POST /authors — create { name, bio? }
3. GET /authors/{id} — detail
4. PUT /authors/{id} — update { name?, bio? }
5. DELETE /authors/{id} — delete

**Books**
1. GET /books?author_id=&year_published= — list (filters optional)
2. POST /books — create { title, year_published?, description?, author_id }
3. GET /books/{id}
4. PUT /books/{id} — update fields same as create
5. DELETE /books/{id}

**Readers**
1. GET /readers
2. POST /readers — create { name, email }
3. GET /readers/{id}
4. PUT /readers/{id} — update { name?, email? }
5. DELETE /readers/{id}

**Stats**
1. GET /stats/popular-books?limit=10
2. GET /stats/popular-authors?limit=10
3. GET /stats/user-total-books
4. GET /stats/user-top-authors?limit=3


**Curl Snippets**
**Health and DB**
1. curl -s http://localhost:8000/health | jq
2. curl -s http://localhost:8000/database/db-ping | jq
3. curl -s http://localhost:8000/database/db-tables | jq

**Authors**
1. curl -s http://localhost:8000/authors | jq
2. curl -s -X POST http://localhost:8000/authors \
  -H 'Content-Type: application/json' \
  -d '{"name":"New Author","bio":"Short bio"}' | jq
3. curl -s http://localhost:8000/authors/1 | jq
4. curl -s -X PUT http://localhost:8000/authors/1 \
  -H 'Content-Type: application/json' \
  -d '{"name":"Updated Name","bio":"Updated bio"}' | jq
5. curl -i -X DELETE http://localhost:8000/authors/1

**Books**
1. curl -s 'http://localhost:8000/books?author_id=1&year_published=1997' | jq
2. curl -s -X POST http://localhost:8000/books \
  -H 'Content-Type: application/json' \
  -d '{"title":"Test Book","year_published":2024,"description":"Demo","author_id":1}' | jq
3. curl -s http://localhost:8000/books/1 | jq
4. curl -s -X PUT http://localhost:8000/books/1 \
  -H 'Content-Type: application/json' \
  -d '{"title":"Updated","year_published":2025,"description":"Updated","author_id":1}' | jq
5. curl -i -X DELETE http://localhost:8000/books/1

**Readers**
1. curl -s http://localhost:8000/readers | jq
2. curl -s -X POST http://localhost:8000/readers \
  -H 'Content-Type: application/json' \
  -d '{"name":"New User","email":"newuser@example.com"}' | jq
3. curl -s http://localhost:8000/readers/1 | jq
4. curl -s -X PUT http://localhost:8000/readers/1 \
  -H 'Content-Type: application/json' \
  -d '{"name":"Updated User","email":"updated@example.com"}' | jq
5. curl -i -X DELETE http://localhost:8000/readers/1


**Running the Tests:**
1. cd into the backend folder
2. Create and activate a virtual environment
3. Install the requirements
4. run pytest -q




