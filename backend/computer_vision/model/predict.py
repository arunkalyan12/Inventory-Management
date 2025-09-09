from pathlib import Path
from ultralytics import YOLO
import cv2

# Path to your trained YOLOv8 model
MODEL_PATH = Path(__file__).parent / "runs/train/exp_yolov8_cuda2/weights/best.pt"

# Load YOLOv8 model
model = YOLO(str(MODEL_PATH))


def predict_image(
    image_path, conf_threshold=0.25, save_result=False, output_dir="predictions"
):
    """
    Predict objects in a single image using YOLOv8.

    Args:
        image_path (str or Path): Path to input image
        conf_threshold (float): Minimum confidence threshold
        save_result (bool): Save image with bounding boxes
        output_dir (str): Directory to save results

    Returns:
        List of detections: [{'label': str, 'confidence': float, 'bbox': [x1, y1, x2, y2]}]
    """
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Run inference
    results = model.predict(str(image_path), conf=conf_threshold)

    detections_list = []
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = box.conf[0].item()
            cls_id = int(box.cls[0].item())
            label = model.names[cls_id]
            detections_list.append(
                {"label": label, "confidence": float(conf), "bbox": [x1, y1, x2, y2]}
            )

    # Optionally save image with bounding boxes
    if save_result:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        img = cv2.imread(str(image_path))
        for det in detections_list:
            x1, y1, x2, y2 = map(int, det["bbox"])
            label = f"{det['label']} {det['confidence']:.2f}"
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                img, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
            )
        save_path = output_dir / image_path.name
        cv2.imwrite(str(save_path), img)
        print(f"Saved prediction image to {save_path}")

    return detections_list


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="YOLOv8 prediction script")
    parser.add_argument("--image", type=str, required=True, help="Path to input image")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold")
    parser.add_argument(
        "--save", action="store_true", help="Save image with predictions"
    )
    args = parser.parse_args()

    preds = predict_image(
        r"C:\Users\arunm\Documents\Projects\Inventory-Management\tests\unit\test.jpg",
        conf_threshold=args.conf,
        save_result=args.save,
    )
    print("Predictions:")
    for pred in preds:
        print(pred)
