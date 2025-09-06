import os
import mlflow
from ultralytics import YOLO


def sanitize_metric_name(name: str) -> str:
    """Sanitize metric names to be MLflow-safe (alphanumeric, _, -, ., /, space)."""
    return "".join(c if c.isalnum() or c in "_-./ " else "_" for c in name)


def log_trained_model_metrics(
    model_path: str,
    data_yaml: str,
    project_dir: str,
    exp_name: str,
    experiment_name: str,
    run_name: str,
):
    """Load a trained YOLO model and log validation/test metrics to MLflow."""

    # Setup MLflow experiment
    mlflow.set_tracking_uri("http://127.0.0.1:8080")
    mlflow.set_experiment(experiment_name)

    # Load the trained model
    model = YOLO(model_path)

    with mlflow.start_run(run_name=run_name):
        # Validation metrics
        val_results = model.val()
        for k, v in val_results.results_dict.items():
            safe_name = sanitize_metric_name(f"val_{k}")
            mlflow.log_metric(safe_name, v)

        # Save best weights artifact
        best_weights_path = os.path.join(project_dir, exp_name, "weights", "best.pt")
        if os.path.exists(best_weights_path):
            mlflow.log_artifact(best_weights_path, artifact_path="models")
            print(f"[INFO] Logged best model weights: {best_weights_path}")
        else:
            print(f"[WARN] Best weights not found at {best_weights_path}")

        # Test set evaluation
        print("[INFO] Running test evaluation...")
        test_results = model.val(data=data_yaml, split="test")
        for k, v in test_results.results_dict.items():
            safe_name = sanitize_metric_name(f"test_{k}")
            mlflow.log_metric(safe_name, v)


if __name__ == "__main__":
    dataset_yaml = "../../shared_utils/shared_utils/config/dataset.yaml"
    trained_model_path = "runs/train/exp_yolov8_cuda2/weights/last.pt"

    log_trained_model_metrics(
        model_path=trained_model_path,
        data_yaml=dataset_yaml,
        project_dir="runs/train",
        exp_name="exp_yolov8_cuda2",
        experiment_name="YOLOv8_Training",
        run_name="log_metrics_only",
    )
