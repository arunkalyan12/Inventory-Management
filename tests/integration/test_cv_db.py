import pytest
from pathlib import Path
from inventory_management.services.cv_inventory_integration import (
    add_cv_predictions_to_inventory,
)
from inventory_management.db.mongo_queries import clear_inventory, ITEMS_COLLECTION
import json


@pytest.fixture(autouse=True)
def cleanup_db():
    # Clear the inventory before and after each test
    clear_inventory()
    yield
    clear_inventory()


def test_add_cv_predictions_to_inventory():
    test_image = Path(__file__).parent / "assets" / "test.jpg"
    assert test_image.exists(), "Test image file does not exist"

    # Call the function directly
    batch_items = add_cv_predictions_to_inventory(
        [str(test_image)], conf_threshold=0.25
    )

    # Print predictions returned by the function
    print("\nPredictions returned by add_cv_predictions_to_inventory:")
    for item in batch_items:
        print(json.dumps(item, indent=2))

    # Check that the batch returned is a list
    assert isinstance(batch_items, list)
    assert len(batch_items) > 0

    # Verify structure and presence in DB
    print("\nItems stored in the database:")
    for item in batch_items:
        assert "name" in item
        assert "quantity" in item
        assert item["quantity"] == 1

        # Check that the item was actually added to the DB
        db_item = ITEMS_COLLECTION.find_one({"name": item["name"]})
        assert db_item is not None
        assert db_item["quantity"] == item["quantity"]
        print(json.dumps(db_item, default=str, indent=2))
