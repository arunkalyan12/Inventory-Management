from fastapi import APIRouter, HTTPException, Response, status, Cookie
from pydantic import BaseModel
from typing import Optional
from passlib.context import CryptContext

from components.inventory_management.db.mongo_queries import (
    insert_user,
    get_user_by_email,
)
from components.inventory_management.db.models import User
from components.inventory_management.core.security import (
    create_access_token,
    verify_access_token,
)
from components.inventory_management.core.config import (
    JWT_SECRET,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

# Import the message queue publisher
from shared_utils.message_queue.mq_client import publish_event

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Models
class SignupRequest(BaseModel):
    full_name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/signup")
def signup(data: SignupRequest, response: Response):
    if get_user_by_email(data.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(data.password)
    user = User(
        email=data.email, full_name=data.full_name, password_hash=hashed_password
    )
    inserted_id = insert_user(user)

    access_token = create_access_token(
        data={"sub": str(inserted_id)}, secret_key=JWT_SECRET
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=False,  # False for dev; True for prod HTTPS
    )

    # --- MQ integration: publish signup event ---
    publish_event("user_signed_up", {"user_id": str(inserted_id), "email": data.email})

    return {"message": "Signup successful", "user_id": str(inserted_id)}


@router.post("/login")
def login(data: LoginRequest, response: Response):
    user = get_user_by_email(data.email)
    if not user or not pwd_context.verify(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(
        data={"sub": str(user.id)}, secret_key=JWT_SECRET
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
    )
    return {"message": "Login successful", "user_id": str(user.id)}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}


@router.get("/me")
def get_current_user(access_token: Optional[str] = Cookie(None)):
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    user_id = verify_access_token(access_token, secret_key=JWT_SECRET)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    return {"user_id": user_id}
