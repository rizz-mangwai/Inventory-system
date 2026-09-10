"""
Inventory service – handles stock levels only.
All AI Assistant logic lives in services/ai_assistant.py
"""

from datetime import datetime


class InventoryService:
    def __init__(self, db):
        self.db = db

    def get_all_with_product(self):
        inventory = self.db.get_inventory()
        products = self.db.get_products()
        product_names = {p["product_id"]: p["name"] for p in products}
        for inv in inventory:
            inv["product_name"] = product_names.get(inv["product_id"], "Unknown")
        return inventory

    def get_low_stock(self):
        products = self.db.get_products()
        return [p for p in products if p["quantity"] <= p["reorder_level"]]

    def update_stock(self, product_id, quantity, operation="add"):
        products = self.db.get_products()
        for p in products:
            if p["product_id"] == product_id:
                if operation == "add":
                    p["quantity"] += quantity
                else:
                    p["quantity"] -= quantity
                self.db.set_products(products)

                inventory = self.db.get_inventory()
                for inv in inventory:
                    if inv["product_id"] == product_id:
                        if operation == "add":
                            inv["quantity_in_stock"] += quantity
                        else:
                            inv["quantity_in_stock"] -= quantity
                        inv["last_updated"] = datetime.now().isoformat()
                        break
                self.db.set_inventory(inventory)
                return True
        return False

    def get_total_inventory_value(self):
        products = self.db.get_products()
        total = 0
        for p in products:
            total += p["quantity"] * p["purchase_price"]
        return total
