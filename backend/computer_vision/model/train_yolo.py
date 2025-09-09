import os
import mlflow
import torch
from ultralytics import YOLO, settings
import re


def sanitize_metric_name(name: str) -> str:
    """Replace invalid characters for MLflow metric names with underscore."""
    return re.sub(r"[^\w\s\-/\.]", "_", name)


def setup_mlflow(
    experiment_name: str, tracking_uri: str = "http://127.0.0.1:8080"
) -> None:
    """Setup MLflow tracking."""
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)


def train_and_log(
    model_name: str,
    experiment_name: str,
    run_name: str,
    data_yaml: str,
    epochs: int = 50,
    img_size: int = 640,
    batch_size: int = 16,
    project_dir: str = "runs/train",  # <- updated base dir
    exp_name: str = "exp_yolov8_cuda2",  # <- updated exp name
    workers: int = 0,
    resume: bool = True,
):
    """Train YOLO model and log everything to MLflow."""

    # Disable YOLO’s built-in MLflow logging
    settings.update({"mlflow": False})

    # Setup MLflow experiment
    setup_mlflow(experiment_name)

    # Device (single GPU or CPU fallback)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[INFO] Training {model_name} on device: {device}")

    # Full checkpoint path
    checkpoint_path = os.path.join(project_dir, exp_name, "weights", "last.pt")

    # Load model (resume if checkpoint exists)
    if resume and os.path.exists(checkpoint_path):
        print(f"[INFO] Resuming training from checkpoint: {checkpoint_path}")
        model = YOLO(checkpoint_path)  # loads weights + optimizer + scheduler\
        resume_flag = True
    else:
        print(f"[INFO] Starting fresh training with model: {model_name}")
        model = YOLO(model_name)
        resume_flag = False

    model.to(device)

    with mlflow.start_run(run_name=run_name):
        # Log params
        mlflow.log_param("model", model_name)
        mlflow.log_param("epochs", epochs)
        mlflow.log_param("img_size", img_size)
        mlflow.log_param("batch_size", batch_size)
        mlflow.log_param("device", device)
        mlflow.log_param("resume", resume_flag)

        # Train
        results = model.train(  # noqa: F841
            data=data_yaml,
            epochs=epochs,
            imgsz=img_size,
            batch=batch_size,
            workers=workers,
            project=project_dir,
            name=exp_name,
            device=0 if device == "cuda" else "cpu",
            resume=resume_flag,
        )  # noqa: F841

        # Validation metrics after training
        val_results = model.val()
        for k, v in val_results.results_dict.items():
            safe_name = sanitize_metric_name(f"val_{k}")
            mlflow.log_metric(safe_name, v)

        # Save best weights
        best_weights_path = os.path.join(project_dir, exp_name, "weights", "best.pt")
        if os.path.exists(best_weights_path):
            mlflow.log_artifact(best_weights_path, artifact_path="models")
            print(f"[INFO] Logged best model weights: {best_weights_path}")
        else:
            print(f"[WARN] Best weights not found at {best_weights_path}")

        # Evaluate on test set
        print(f"[INFO] Running {model_name} test evaluation...")
        test_results = model.val(data=data_yaml, split="test")
        for k, v in test_results.results_dict.items():
            safe_name = sanitize_metric_name(f"test_{k}")
            mlflow.log_metric(safe_name, v)


def main():
    """Main entry point."""
    dataset_yaml = "../../shared_utils/shared_utils/config/dataset.yaml"

    train_and_log(
        model_name="yolov8m.pt",
        experiment_name="YOLOv8_Training",
        run_name="yolov8_resume_cuda2",
        data_yaml=dataset_yaml,
        exp_name="exp_yolov8_cuda2",  # same exp name as checkpoint dir
        resume=True,
    )


if __name__ == "__main__":
    main()
