from fastapi import FastAPI
from threading import Thread
from pathlib import Path

from typing import Optional
from .routes import router as inventory_router
from .auth import router as auth_router
from .event_listener import start_listener_blocking, stop_listener
from dotenv import load_dotenv

# Load env (adjust path if your dev.env is at repo root)
load_dotenv(
    dotenv_path=Path(__file__).resolve().parents[3] / "config/environment/dev.env"
)

app = FastAPI(title="Inventory Management Service")

# Include routers (set prefixes as desired)
app.include_router(auth_router, prefix="/auth")
app.include_router(inventory_router, prefix="/api")

# We'll run the listener in a background thread
_listener_thread: Optional[Thread] = None


@app.on_event("startup")
def startup_event():
    global _listener_thread
    # Start MQ event listener in a daemon thread
    _listener_thread = Thread(target=start_listener_blocking, daemon=True)
    _listener_thread.start()


@app.on_event("shutdown")
def shutdown_event():
    # Stop MQ listener gracefully
    stop_listener()
    # thread is daemon — process exit will terminate it
