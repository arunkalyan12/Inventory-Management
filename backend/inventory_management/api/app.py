# backend/inventory_management/api/app.py

from fastapi import FastAPI
from threading import Thread
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Import routers
from .routes import router as inventory_router
from .auth import router as auth_router
from .event_listener import start_listener_blocking, stop_listener

# Load environment variables from config/environment/dev.env
load_dotenv(
    dotenv_path=Path(__file__).resolve().parents[3] / "config/environment/dev.env"
)

# Initialize FastAPI app
app = FastAPI(title="Inventory Management Service")

# Register routers with URL prefixes
app.include_router(auth_router, prefix="/auth")
app.include_router(inventory_router, prefix="/api")

# Background thread for event listener
_listener_thread: Optional[Thread] = None


@app.on_event("startup")
def startup_event():
    global _listener_thread
    print("Starting up Inventory Management Service...")
    # Start the event listener in a separate daemon thread
    _listener_thread = Thread(target=start_listener_blocking, daemon=True)
    _listener_thread.start()


@app.on_event("shutdown")
def shutdown_event():
    print("Shutting down Inventory Management Service...")
    stop_listener()
