from fastapi import FastAPI
from components.inventory_management.api.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router, prefix="/api")
