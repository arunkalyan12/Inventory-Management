from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
from components.inventory_management.core.config import (
    JWT_SECRET,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

ALGORITHM = "HS256"


def create_access_token(
    data: dict, expires_delta: timedelta = None, secret_key: str = JWT_SECRET
) -> str:
    """
    Generate a JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)


def verify_access_token(token: str, secret_key: str = JWT_SECRET) -> Optional[str]:
    """
    Verify JWT token and return user_id (sub) if valid.
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        return user_id
    except JWTError:
        return None
