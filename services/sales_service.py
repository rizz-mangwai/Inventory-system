from datetime import datetime


class SalesService:
    def __init__(self, db):
        self.db = db

    def _get_next_id(self):
        sales = self.db.get_sales()
        if not sales:
            return 1
        return max(s["sale_id"] for s in sales) + 1

    def record_sale(self, product_id, customer_id, quantity, sale_price, date=None):
        if date is None:
            date = datetime.now().date().isoformat()

        # Check stock is available
        products = self.db.get_products()
        product = None
        for p in products:
            if p["product_id"] == product_id:
                product = p
                break
        if not product:
            return None
        if product["quantity"] < quantity:
            return None

        # Reduce stock
        product["quantity"] -= quantity
        self.db.set_products(products)

        # Record the sale
        sale = {
            "sale_id": self._get_next_id(),
            "product_id": product_id,
            "customer_id": customer_id,
            "quantity": quantity,
            "sale_price": sale_price,
            "date": date
        }
        sales = self.db.get_sales()
        sales.append(sale)
        self.db.set_sales(sales)

        # Keep inventory record in sync
        inventory = self.db.get_inventory()
        for inv in inventory:
            if inv["product_id"] == product_id:
                inv["quantity_in_stock"] -= quantity
                inv["last_updated"] = datetime.now().isoformat()
                break
        self.db.set_inventory(inventory)

        return sale["sale_id"]

    def get_all(self):
        sales = self.db.get_sales()
        for s in sales:
            s["product_name"] = self._get_product_name(s["product_id"])
            s["customer_name"] = self._get_customer_name(s["customer_id"])
        return sales

    def get_by_product(self, product_id):
        sales = self.db.get_sales()
        results = []
        for s in sales:
            if s["product_id"] == product_id:
                s["customer_name"] = self._get_customer_name(s["customer_id"])
                results.append(s)
        return results

    def get_by_customer(self, customer_id):
        sales = self.db.get_sales()
        results = []
        for s in sales:
            if s["customer_id"] == customer_id:
                s["product_name"] = self._get_product_name(s["product_id"])
                results.append(s)
        return results

    def get_total_sales_value(self):
        sales = self.db.get_sales()
        total = 0
        for s in sales:
            total += s["quantity"] * s["sale_price"]
        return total

    def get_sales_by_product(self):
        sales = self.db.get_sales()
        summary = {}
        for s in sales:
            pid = s["product_id"]
            if pid not in summary:
                summary[pid] = {"total_qty": 0, "total_value": 0}
            summary[pid]["total_qty"] += s["quantity"]
            summary[pid]["total_value"] += s["quantity"] * s["sale_price"]
        result = []
        for pid, data in summary.items():
            result.append({
                "product_name": self._get_product_name(pid),
                "total_qty": data["total_qty"],
                "total_value": data["total_value"]
            })
        return sorted(result, key=lambda x: x["total_qty"], reverse=True)

    def _get_product_name(self, product_id):
        products = self.db.get_products()
        for p in products:
            if p["product_id"] == product_id:
                return p["name"]
        return "Unknown"

    def _get_customer_name(self, customer_id):
        if customer_id == 0:
            return "None"
        customers = self.db.get_customers()
        for c in customers:
            if c["customer_id"] == customer_id:
                return c["name"]
        return "Unknown"
