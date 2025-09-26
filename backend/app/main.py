from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models, seed
from .db import Base, get_db, engine
from sqlalchemy.orm import Session
from .routers import debug, authors, books, readers

app = FastAPI(title="Subtera Library Assessment API", version="1.0.0")

#React dev server --> Vite default is port 5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(debug.router)
app.include_router(authors.router)
app.include_router(books.router)    
app.include_router(readers.router)  

@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

@app.on_event("startup")
def on_startup():
    """Create database tables on startup and loads seed data"""
    #Create the tables
    Base.metadata.create_all(bind=engine)
    
    #Seed the database
    db: Session = next(get_db())
    try:
        seed.seed_database(db)
    finally:
        db.close()