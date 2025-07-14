import os
import shutil

# Source and target paths
source_path = r"C:\Users\arunm\Documents\ML Tools\OIDv4_ToolKit\OID\Dataset"
target_path = r"C:\Users\arunm\Documents\Projects\Inventory-Management\components\computer_vision\data\Raw Data"

# Make sure the target path exists
os.makedirs(target_path, exist_ok=True)

# Folders to move
folders_to_move = ['train', 'test']

for folder in folders_to_move:
    src_folder = os.path.join(source_path, folder)
    dst_folder = os.path.join(target_path, folder)

    if os.path.exists(src_folder):
        # Move the folder
        print(f"Moving {src_folder} to {dst_folder}")
        shutil.move(src_folder, dst_folder)
    else:
        print(f"Source folder does not exist: {src_folder}")
