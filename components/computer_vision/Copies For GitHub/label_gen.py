import csv
import os

# ========================
# CONFIG
# ========================
CSV_PATH = r"C:\Users\arunm\Documents\ML Tools\OIDv4_ToolKit\OID\csv_folder\class-descriptions-boxable.csv"
OUTPUT_CLASSES = r"C:\Users\arunm\Documents\Projects\Inventory-Management\data\yolo_data\classes.txt"

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

# ========================
# STEP 1: Load valid OID classes
# ========================
valid_classes = set()
with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        valid_classes.add(row[1])  # class name is in 2nd column

# ========================
# STEP 2: Filter
# ========================
filtered_classes = [cls for cls in desired_classes if cls in valid_classes]

print(f"✅ Total valid classes found: {len(filtered_classes)}")

# ========================
# STEP 3: Save classes.txt
# ========================
os.makedirs(os.path.dirname(OUTPUT_CLASSES), exist_ok=True)
with open(OUTPUT_CLASSES, "w", encoding="utf-8") as f:
    for cls in filtered_classes:
        f.write(cls + "\n")

print(f"📄 classes.txt saved at: {OUTPUT_CLASSES}")
