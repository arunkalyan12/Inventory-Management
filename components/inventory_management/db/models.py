# models.py
from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field


class InventoryItem(BaseModel):
    id: Optional[str] = Field(None, alias="id")
    name: str
    category_id: str
    location_id: str
    quantity: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        data = self.model_dump(by_alias=True)
        if "id" in data and data["id"] is None:
            del data["id"]
        return data


class Category(BaseModel):
    id: Optional[str] = Field(None, alias="id")
    name: str
    description: Optional[str] = ""

    def to_dict(self):
        data = self.model_dump(by_alias=True)
        if "id" in data and data["id"] is None:
            del data["id"]
        return data


class Location(BaseModel):
    id: Optional[str] = Field(None, alias="id")
    name: str
    description: Optional[str] = ""

    def to_dict(self):
        data = self.model_dump(by_alias=True)
        if "id" in data and data["id"] is None:
            del data["id"]
        return data


class User(BaseModel):
    id: Optional[str] = Field(None, alias="id")
    full_name: str
    email: str
    password_hash: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        data = self.model_dump(by_alias=True)
        if "id" in data and data["id"] is None:
            del data["id"]
        return data


class ShoppingListItem(BaseModel):
    id: Optional[str] = Field(None, alias="id")
    user_id: str
    item_name: str
    quantity: int = 1
    purchased: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        data = self.model_dump(by_alias=True)
        if "id" in data and data["id"] is None:
            del data["id"]
        return data
