import csv
import subprocess
import time

# Path to your downloaded Open Images class descriptions
CSV_PATH = r"C:\Users\arunm\OneDrive\Documents\ML Tools\OIDv4_ToolKit\OID\csv_folder\class-descriptions-boxable.csv"


# Your grocery-related classes (replace or expand as needed)
desired_classes = [
    "Apple", "Banana", "Orange", "Strawberry", "Pineapple", "Mango", "Watermelon",
    "Grapefruit", "Lemon", "Lime", "Grape", "Pear", "Peach", "Plum", "Kiwi",
    "Tomato", "Potato", "Carrot", "Cucumber", "Broccoli", "Onion", "Garlic", "Lettuce",
    "Spinach", "Cabbage", "Corn", "Pumpkin", "Zucchini", "Bell pepper", "Eggplant",
    "Chili pepper", "Radish", "Mushroom", "Green beans", "Meat", "Beef", "Chicken",
    "Pork", "Sausage", "Bacon", "Ham", "Turkey", "Fish", "Seafood", "Shrimp", "Egg",
    "Milk", "Cheese", "Yogurt", "Butter", "Bread", "Croissant", "Bagel", "Doughnut",
    "Cake", "Pie", "Cookie", "Rice", "Pasta", "Noodles", "Pizza", "Burger", "Hot dog",
    "Sandwich", "Bottle", "Can", "Carton", "Canned food", "Packaged goods", "Bowl",
    "Food", "Snack", "Ice cream", "Candy", "Soda", "Coffee", "Tea", "Juice"
]

# Load valid Open Images classes into a set for fast lookup
valid_classes = set()
with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        valid_classes.add(row[1])  # class name is the second column

# Filter to only include valid classes
filtered_classes = [cls for cls in desired_classes if cls in valid_classes]

print(f"Total valid classes found: {len(filtered_classes)}")


# Convert multi-word names to underscore format (as required by OIDv4_ToolKit)
def format_class_name(name):
    return name.replace(" ", "_")


# Download in batches of 5
batch_size = 5
for i in range(0, len(filtered_classes), batch_size):
    batch = filtered_classes[i:i + batch_size]
    formatted = [format_class_name(cls) for cls in batch]
    command = [
                  "python", "main.py", "downloader",
                  "--classes"
              ] + formatted + [
                  "--type_csv", "train", #change test to train for train files
                  "--limit", "300",
                  "--multiclasses", "1"
              ]

    print(f"\nDownloading batch: {', '.join(batch)}")
    subprocess.run(command)
    time.sleep(3)