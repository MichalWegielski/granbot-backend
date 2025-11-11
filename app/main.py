"""
Main FastAPI application entry point.
Initializes the app, loads data at startup, and registers routes.
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from app.routes import sections_controller
from app.services import data_service

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    Loads documents from JSONL file on startup.
    """
    # Startup: Load documents
    print("Starting up: Loading documents...")
    data_service.load_documents()
    print("Startup complete.")
    
    yield
    
    # Shutdown: Cleanup if needed
    print("Shutting down...")


# Create FastAPI application
app = FastAPI(
    title="Grantbot Backend",
    description="Backend API for grant application section generation",
    version="1.0.0",
    lifespan=lifespan
)

# Register routes
app.include_router(sections_controller.router, tags=["sections"])


@app.get("/")
def root():
    """Root endpoint for health check."""
    return {
        "message": "Grantbot Backend API",
        "status": "running"
    }

