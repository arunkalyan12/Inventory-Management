from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT_DIR / "computer_vision" / "data"
RAW_DATA_DIR = DATA_DIR / "Raw Data"
RAW_TRAIN_DIR = RAW_DATA_DIR / "train"
RAW_TEST_DIR = RAW_DATA_DIR / "test"
FINAL_DATA_DIR = DATA_DIR / "Final Data"
# Models
MODELS_DIR = ROOT_DIR / "components" / "computer_vision" / "model"