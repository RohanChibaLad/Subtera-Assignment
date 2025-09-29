from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from . import models, seed
from .db import Base, SessionLocal, engine
from sqlalchemy.orm import Session
from .routers import database, authors, books, readers, stats
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on startup and loads seed data"""
    #Create the tables
    Base.metadata.create_all(bind=engine)
    
    if os.getenv("SKIP_STARTUP_SEED") != "1":
        with SessionLocal() as db:  # use SessionLocal, not next(get_db())
            seed.seed_database(db)  # make sure this commits internally

    # hand control back to FastAPI
    yield

app = FastAPI(title="Subtera Library Assessment API", version="1.0.0", lifespan=lifespan)

#React dev server --> Vite default is port 5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(database.router)
app.include_router(authors.router)
app.include_router(books.router)    
app.include_router(readers.router)  
app.include_router(stats.router)

@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
