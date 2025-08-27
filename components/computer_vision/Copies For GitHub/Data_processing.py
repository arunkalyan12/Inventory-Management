import os
import shutil
from PIL import Image
from shared_utils.config.path import RAW_DATA_DIR, FINAL_DATA_DIR

# ========================
# CONFIG
# ========================
RAW_DATA = RAW_DATA_DIR      # raw OID data ("Raw Data")
OUTPUT_DIR = FINAL_DATA_DIR  # Final Data will act as YOLO-ready dataset
CLASSES_FILE = FINAL_DATA_DIR / "classes.txt"
SPLITS = ["train", "test"]   # OIDv4: test -> val

def load_classes(classes_file):
    if not classes_file.exists():
        raise FileNotFoundError(f"❌ classes.txt not found at {classes_file}")
    return [line.strip() for line in classes_file.read_text().splitlines() if line.strip()]

def build_class_mapping(classes):
    return {cls: i for i, cls in enumerate(classes)}

def convert_label(label_path, image_path, class_mapping):
    yolo_lines = []
    with open(label_path, "r") as f:
        lines = f.readlines()

    img = Image.open(image_path)
    img_w, img_h = img.size

    for line in lines:
        parts = line.strip().split()
        if len(parts) != 5:
            continue
        cls_name, x_min, y_min, x_max, y_max = parts
        if cls_name not in class_mapping:
            continue

        cls_id = class_mapping[cls_name]
        x_min, y_min, x_max, y_max = map(float, (x_min, y_min, x_max, y_max))

        # YOLO format
        x_center = ((x_min + x_max) / 2) / img_w
        y_center = ((y_min + y_max) / 2) / img_h
        width = (x_max - x_min) / img_w
        height = (y_max - y_min) / img_h

        yolo_lines.append(f"{cls_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

    return yolo_lines

def process_dataset(raw_data, output_dir, class_mapping):
    for split in SPLITS:
        split_dir = raw_data / split
        yolo_split = "val" if split == "test" else "train"

        img_out_dir = output_dir / "images" / yolo_split
        lbl_out_dir = output_dir / "labels" / yolo_split
        os.makedirs(img_out_dir, exist_ok=True)
        os.makedirs(lbl_out_dir, exist_ok=True)

        for folder in os.listdir(split_dir):
            folder_path = split_dir / folder
            label_folder = folder_path / "Label"

            if not folder_path.is_dir():
                continue

            for file in os.listdir(folder_path):
                if file.lower().endswith((".jpg", ".jpeg", ".png")):
                    img_path = folder_path / file
                    label_path = label_folder / f"{os.path.splitext(file)[0]}.txt"

                    if not label_path.exists():
                        continue

                    yolo_labels = convert_label(label_path, img_path, class_mapping)
                    if not yolo_labels:
                        continue

                    shutil.copy(img_path, img_out_dir / file)

                    with open(lbl_out_dir / f"{os.path.splitext(file)[0]}.txt", "w") as f:
                        f.write("\n".join(yolo_labels))

    print(f"✅ Dataset converted to YOLO format at: {output_dir}")


if __name__ == "__main__":
    print("📄 Loading classes from file...")
    classes = load_classes(CLASSES_FILE)
    print("Found classes:", classes)

    print("📄 Building mapping...")
    class_mapping = build_class_mapping(classes)

    print("⚙️ Processing dataset...")
    process_dataset(RAW_DATA, OUTPUT_DIR, class_mapping)