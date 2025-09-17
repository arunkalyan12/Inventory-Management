from computer_vision.model.predict import predict_image
from inventory_management.db.mongo_queries import (
    add_inventory_batch,
)  # Your DB batch insert


def add_cv_predictions_to_inventory(image_paths, conf_threshold=0.25):
    """
    Takes a list of image paths, predicts items with YOLOv8, converts
    predictions to inventory format, and adds them to the DB in batch.
    """
    batch_items = []

    for img_path in image_paths:
        detections = predict_image(img_path, conf_threshold=conf_threshold)

        for det in detections:
            # Map label -> inventory format
            item = {
                "name": det["label"],  # Use YOLO label
                "quantity": 1,  # Default quantity
                "category": "Uncategorized",  # Optional, can improve later
                "confidence": det["confidence"],  # Optional
            }
            batch_items.append(item)

    if batch_items:
        add_inventory_batch(batch_items)  # Insert all at once

    return batch_items
