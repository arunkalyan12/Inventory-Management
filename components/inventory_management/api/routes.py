from fastapi import APIRouter, HTTPException, Depends, Cookie, status
from typing import Optional
from components.inventory_management.db import mongo_queries as mq
from components.inventory_management.api.auth import verify_access_token
from components.inventory_management.core.config import JWT_SECRET

router = APIRouter(prefix="/api", tags=["inventory"])


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
    return user_id


@router.get("/items")
def list_items(current_user: str = Depends(get_current_user)):
    items = mq.get_all_items()
    return {"items": items}


@router.post("/items")
def create_item(item: dict, current_user: str = Depends(get_current_user)):
    new_item = mq.insert_item(item)
    return {"message": "Item created", "item_id": str(new_item.inserted_id)}
