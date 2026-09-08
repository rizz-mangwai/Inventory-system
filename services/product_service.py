"""
Simple product service – works with dictionaries, not SQL.
"""

from datetime import datetime


class ProductService:
    def __init__(self, db):
        self.db = db

    def _get_next_id(self):
        products = self.db.get_products()
        if not products:
            return 1
        return max(p["product_id"] for p in products) + 1

    def add(self, name, category_id, supplier_id, price, purchase_price,
            quantity, reorder_level, description=""):
        product_id = self._get_next_id()
        product = {
            "product_id": product_id,
            "name": name,
            "category_id": category_id,
            "supplier_id": supplier_id,
            "price": price,
            "purchase_price": purchase_price,
            "quantity": quantity,
            "reorder_level": reorder_level,
            "description": description
        }
        products = self.db.get_products()
        products.append(product)
        self.db.set_products(products)

        # Also create a matching inventory record
        inventory = self.db.get_inventory()
        inventory.append({
            "inventory_id": len(inventory) + 1,
            "product_id": product_id,
            "quantity_in_stock": quantity,
            "last_updated": datetime.now().isoformat()
        })
        self.db.set_inventory(inventory)
        return product_id

    def get_all(self):
        products = self.db.get_products()
        # Add category and supplier names for easy display
        for p in products:
            p["category_name"] = self._get_category_name(p["category_id"])
            p["supplier_name"] = self._get_supplier_name(p["supplier_id"])
        return products

    def get_by_id(self, product_id):
        products = self.db.get_products()
        for p in products:
            if p["product_id"] == product_id:
                return p
        return None

    def search(self, keyword):
        keyword = keyword.lower()
        products = self.db.get_products()
        results = []
        for p in products:
            if keyword in p["name"].lower() or keyword in p["description"].lower():
                results.append(p)
        return results

    def update(self, product_id, **kwargs):
        products = self.db.get_products()
        for p in products:
            if p["product_id"] == product_id:
                for key, value in kwargs.items():
                    if key in p:
                        p[key] = value
                self.db.set_products(products)
                # Keep inventory in sync
                inventory = self.db.get_inventory()
                for inv in inventory:
                    if inv["product_id"] == product_id:
                        inv["quantity_in_stock"] = kwargs.get("quantity", p["quantity"])
                        inv["last_updated"] = datetime.now().isoformat()
                        break
                self.db.set_inventory(inventory)
                return True
        return False

    def delete(self, product_id):
        # Don't allow deleting a product that already has sales history
        sales = self.db.get_sales()
        for s in sales:
            if s["product_id"] == product_id:
                return False
        products = self.db.get_products()
        products = [p for p in products if p["product_id"] != product_id]
        self.db.set_products(products)
        inventory = self.db.get_inventory()
        inventory = [i for i in inventory if i["product_id"] != product_id]
        self.db.set_inventory(inventory)
        return True

    def _get_category_name(self, category_id):
        categories = self.db.get_categories()
        for c in categories:
            if c["category_id"] == category_id:
                return c["name"]
        return "Unknown"

    def _get_supplier_name(self, supplier_id):
        suppliers = self.db.get_suppliers()
        for s in suppliers:
            if s["supplier_id"] == supplier_id:
                return s["name"]
        return "Unknown"
