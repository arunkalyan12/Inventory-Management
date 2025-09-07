import pytest
from pathlib import Path
from components.computer_vision.model import predict
import cv2
import numpy as np


# ----------------------------
# Fixture: use local real test image
# ----------------------------
@pytest.fixture(scope="session")
def test_image():
    """Return path to real test image of an apple."""
    img_path = Path(__file__).parent / "test.jpg"
    if not img_path.exists():
        raise FileNotFoundError(f"Test image not found: {img_path}")
    return img_path


# ----------------------------
# Test 1: Run real YOLO prediction
# ----------------------------
def test_predict_image_real(test_image):
    """Test YOLO prediction on a real image and validate expected class IDs."""
    preds = predict.predict_image(test_image, conf_threshold=0.5, save_result=False)
    print(preds)

    assert isinstance(preds, list)
    assert len(preds) > 0, "Expected at least one prediction"

    # Ensure each prediction has required keys
    for pred in preds:
        assert "label" in pred
        assert "confidence" in pred
        assert "bbox" in pred

    # Check that at least one prediction is an apple (class_id 0)
    label = [pred["label"] for pred in preds]
    assert "Apple" in label, f"Expected apple in predictions, got: {label}"


# ----------------------------
# Test 2: Saving prediction image
# ----------------------------
def test_predict_image_save(test_image, tmp_path):
    """Test YOLO prediction saves output image."""
    output_dir = tmp_path / "preds"
    preds = predict.predict_image(
        test_image, conf_threshold=0.5, save_result=True, output_dir=output_dir
    )

    assert isinstance(preds, list)

    saved_files = list(output_dir.glob("*"))
    assert len(saved_files) == 1
    assert saved_files[0].name == test_image.name


# ----------------------------
# Test 3: Dummy black image
# ----------------------------
@pytest.fixture
def dummy_image(tmp_path):
    """Create a dummy black image."""
    img_path = tmp_path / "dummy.jpg"
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.imwrite(str(img_path), img)
    return img_path


def test_predict_image_file_not_found():
    """Test prediction with non-existing file."""
    with pytest.raises(FileNotFoundError):
        predict.predict_image("non_existing_file.jpg")


# from pathlib import Path
# from components.computer_vision.model import predict
#
# # Path to your test image
# test_image = Path(r"C:\Users\arunm\Documents\Projects\Inventory-Management\tests\unit\test.jpg")
#
# # Run prediction
# predictions = predict.predict_image(test_image, conf_threshold=0.25, save_result=True)
#
# # Print output
# print("\nPredictions:")
# print(predictions)
