from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from components.inventory_management.db.mongo_queries import (
    insert_user,
    get_user_by_email,
)
from components.inventory_management.db.models import User
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SignupRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/signup")
def signup(data: SignupRequest):
    if get_user_by_email(data.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(data.password)

    user = User(email=data.email, full_name="Test User", password_hash=hashed_password)

    # make sure insert_user returns the inserted ObjectId
    inserted_id = insert_user(user)

    return {"message": "Signup successful", "user_id": str(inserted_id)}


@router.post("/login")
def login(data: LoginRequest):
    user = get_user_by_email(data.email)
    if not user or not pwd_context.verify(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {"message": "Login successful", "user_id": str(user.id)}
