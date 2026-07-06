import csv
import logging
from dataclasses import dataclass, field
from typing import List, Dict

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@dataclass
class LowStockAlert:
    sku: str
    name: str
    on_hand: int
    safety_threshold: int
    reorder_qty: int
    unit_cost: float
    vendor: str
    est_reorder_cost: float = field(init=False)

    def __post_init__(self):
        self.est_reorder_cost = round(self.reorder_qty * self.unit_cost, 2)


def load_inventory_from_csv(file_path: str) -> List[Dict]:
    """Loads inventory items from a CSV file. Parses numeric columns."""
    inventory = []
    try:
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                inventory.append({
                    "sku": row["sku"].strip(),
                    "name": row["name"].strip(),
                    "on_hand": int(row["on_hand"]),
                    "safety_threshold": int(row["safety_threshold"]),
                    "reorder_qty": int(row["reorder_qty"]),
                    "unit_cost": float(row["unit_cost"]),
                    "vendor": row["vendor"].strip()
                })
    except FileNotFoundError:
        logging.error(f"Inventory CSV file not found at {file_path}")
        raise
    except (ValueError, KeyError) as e:
        logging.error(f"Error parsing inventory CSV structure or data types: {e}")
        raise
    return inventory


def run_inventory_tracker(inventory: List[Dict]) -> List[LowStockAlert]:
    """Scans inventory and returns alerts for items below safety thresholds."""
    print("\n=== FRAGMENT 1: Inventory Tracker ===")
    print("Scanning warehouse/stock logs against safety thresholds...\n")
    alerts = []
    for item in inventory:
        status = "OK"
        if item["on_hand"] < item["safety_threshold"]:
            status = "LOW STOCK"
            alert = LowStockAlert(
                sku=item["sku"],
                name=item["name"],
                on_hand=item["on_hand"],
                safety_threshold=item["safety_threshold"],
                reorder_qty=item["reorder_qty"],
                unit_cost=item["unit_cost"],
                vendor=item["vendor"]
            )
            alerts.append(alert)
        print(f"  [{status:9}] {item['sku']:10} {item['name']:24} on_hand={item['on_hand']:<5} threshold={item['safety_threshold']}")

    print(f"\n>> Fragment 1 complete: {len(alerts)} item(s) below safety threshold.")
    return alerts
