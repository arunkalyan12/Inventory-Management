from fastapi import APIRouter, HTTPException

router = APIRouter()

shopping_list = [
    {"id": 1, "name": "Batteries", "quantity": 2},
    {"id": 2, "name": "Charger", "quantity": 1},
]


@router.get("/", summary="Get all shopping list items")
def get_shopping_list():
    return {"shopping_list": shopping_list}


@router.get("/{item_id}", summary="Get a specific shopping list item")
def get_shopping_item(item_id: int):
    item = next((item for item in shopping_list if item["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/", summary="Add a new item to the shopping list")
def add_shopping_item(item: dict):
    item["id"] = len(shopping_list) + 1
    shopping_list.append(item)
    return item


@router.put("/{item_id}", summary="Update an existing shopping list item")
def update_shopping_item(item_id: int, updated_item: dict):
    for idx, item in enumerate(shopping_list):
        if item["id"] == item_id:
            shopping_list[idx].update(updated_item)
            shopping_list[idx]["id"] = item_id
            return shopping_list[idx]
    raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/{item_id}", summary="Delete a shopping list item")
def delete_shopping_item(item_id: int):
    global shopping_list
    shopping_list = [item for item in shopping_list if item["id"] != item_id]
    return {"message": "Item deleted successfully"}
