from ..db.mongo_queries import get_item_by_id, list_items, get_items_by_category

def get_item(item_id: str):
    return get_item_by_id(item_id)


def list_all_items(filters: dict = None):
    return list_items(filters)


def list_items_by_category(category_id: str):
    return get_items_by_category(category_id)