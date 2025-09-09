from fastapi import APIRouter, HTTPException

router = APIRouter()

inventory_items = [
    {"id": 1, "name": "Laptop", "quantity": 5},
    {"id": 2, "name": "Phone", "quantity": 10},
]


@router.get("/", summary="Get all inventory items")
def get_inventory():
    return {"inventory": inventory_items}


@router.get("/{item_id}", summary="Get a specific inventory item")
def get_inventory_item(item_id: int):
    item = next((item for item in inventory_items if item["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/", summary="Add a new inventory item")
def add_inventory_item(item: dict):
    item["id"] = len(inventory_items) + 1
    inventory_items.append(item)
    return item


@router.put("/{item_id}", summary="Update an existing inventory item")
def update_inventory_item(item_id: int, updated_item: dict):
    for idx, item in enumerate(inventory_items):
        if item["id"] == item_id:
            inventory_items[idx].update(updated_item)
            inventory_items[idx]["id"] = item_id
            return inventory_items[idx]
    raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/{item_id}", summary="Delete an inventory item")
def delete_inventory_item(item_id: int):
    global inventory_items
    inventory_items = [item for item in inventory_items if item["id"] != item_id]
    return {"message": "Item deleted successfully"}
