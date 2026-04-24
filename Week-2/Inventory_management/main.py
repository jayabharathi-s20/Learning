import csv
import logging
from datetime import datetime
from abc import ABC, abstractmethod
from fastapi import FastAPI

from validator import Item

# ---------------- LOGGING ----------------------------------
logging.basicConfig(
    filename="errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------- FASTAPI APP -------------------------------
app = FastAPI()

# ---------------- READ CSV -----------------------------------
def read_inventory(file_path):
    items = []

    with open(file_path, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                item = Item(
                    item_id=int(row["item_id"]),
                    name=row["name"],
                    quantity=int(row["quantity"]),
                    threshold=int(row["threshold"]),
                    price=float(row["price"]),
                    category=row["category"],
                    supplier=row["supplier"],
                    expiry_date=datetime.strptime(
                        row["expiry_date"], "%Y-%m-%d"
                    ).date()
                )
                items.append(item)

            except Exception as e:
                logging.error(f"Error in row {row}: {e}")

    return items

# ---------------- LOW STOCK REPORT (OCP EXTENSION) ----------------
class LowStockReport():
    def generate(self, items):
        return [
            item for item in items
            if item.quantity <= item.threshold
        ]

# ---------------- GET ALL ITEMS ------------------------------------
@app.get("/get-items")
def get_items():
    return read_inventory("inventory.csv")

# ---------------- ADD ITEM TO CSV ----------------------------------
@app.post("/post-items")
def add_item(item: Item):
    try:
        with open("inventory.csv", "a", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                item.item_id,
                item.name,
                item.quantity,
                item.threshold,
                item.price,
                item.category,
                item.supplier,
                item.expiry_date
            ])

        return {"message": "Item added successfully", "item": item}

    except Exception as e:
        logging.error(f"Error adding item: {e}")
        return {"error": "Failed to add item"}

# ---------------- LOW STOCK API ---------------------------------------
@app.get("/reports/low-stock")
def low_stock():
    items = read_inventory("inventory.csv")

    report = LowStockReport()
    return report.generate(items)