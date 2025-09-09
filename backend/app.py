# backend/app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .inventory_management.api.auth import router as auth_router
from .inventory_management.api.inventory import router as inventory_router
from .inventory_management.api.shopping_list import router as shopping_router
from shared_utils.logging.logger import get_logger

logger = get_logger("backend_app")

app = FastAPI(
    title="Inventory Management System",
    description="API for inventory management, shopping lists, and users",
    version="1.0.0",
)

# ---- Middleware ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Include Routers ----
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(inventory_router, prefix="/inventory", tags=["Inventory"])
app.include_router(shopping_router, prefix="/shopping-list", tags=["Shopping List"])


# ---- Root Endpoint ----
@app.get("/")
def root():
    return {"message": "Inventory Management API is running!"}


# ---- Startup / Shutdown events ----
@app.on_event("startup")
def startup_event():
    logger.info("Backend starting up...")


@app.on_event("shutdown")
def shutdown_event():
    logger.info("Backend shutting down...")
