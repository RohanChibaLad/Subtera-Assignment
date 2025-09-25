from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .db import Base, get_db, engine
from sqlalchemy.orm import Session
from .routers import debug

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

@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

@app.on_event("startup")
def on_startup():
    """Create database tables on startup."""
    Base.metadata.create_all(bind=engine)