"""
AI Assistant – helps the shop owner see which products are moving fast,
which are stuck on the shelf, which are about to run out, which are
sitting in excess, and how much to reorder.

This is "rule-based AI": no external ML library needed. It works out
each product's sales velocity (average units sold per day) from the
sales history, then uses that number to answer five business
questions. That's exactly the kind of thing a real store manager
would do by hand with a spreadsheet — this just automates it.
"""

from datetime import datetime, timedelta


class AIAssistant:
    def __init__(self, db):
        self.db = db

    # ---------- Shared helper ----------
    def _sales_in_period(self, days):
        """Return {product_id: total_units_sold} for the last `days` days."""
        cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        sales = self.db.get_sales()
        totals = {}
        for s in sales:
            if s["date"] >= cutoff:
                pid = s["product_id"]
                totals[pid] = totals.get(pid, 0) + s["quantity"]
        return totals

    def _sales_velocity(self, product_id, days=30):
        """Average units sold per day over the period, for one product."""
        totals = self._sales_in_period(days)
        total_units = totals.get(product_id, 0)
        return total_units / days if days > 0 else 0

    # ---------- 1. Fast-Moving Products ----------
    def get_fast_moving_products(self, days=30, min_sales=5):
        """Products that sold at least `min_sales` units in the period."""
        totals = self._sales_in_period(days)
        products = self.db.get_products()
        result = []
        for p in products:
            total = totals.get(p["product_id"], 0)
            if total >= min_sales:
                result.append({
                    "product_id": p["product_id"],
                    "name": p["name"],
                    "total_sold_period": total,
                    "sales_velocity": total / days if days > 0 else 0
                })
        return sorted(result, key=lambda x: x["sales_velocity"], reverse=True)

    # ---------- 2. Slow-Moving Products ----------
    def get_slow_moving_products(self, days=30, max_sales=1):
        """Products that sold `max_sales` units or fewer in the period."""
        totals = self._sales_in_period(days)
        products = self.db.get_products()
        result = []
        for p in products:
            total = totals.get(p["product_id"], 0)
            if total <= max_sales:
                result.append({
                    "product_id": p["product_id"],
                    "name": p["name"],
                    "total_sold_period": total,
                    "sales_velocity": total / days if days > 0 else 0
                })
        return sorted(result, key=lambda x: x["total_sold_period"])

    # ---------- 3. Stockout Risk ----------
    def get_stockout_risk(self, days=30, days_left_threshold=5):
        """Products projected to run out within `days_left_threshold` days,
        based on how fast they've been selling."""
        products = self.db.get_products()
        result = []
        for p in products:
            velocity = self._sales_velocity(p["product_id"], days)
            if velocity > 0:
                days_left = p["quantity"] / velocity
                if days_left < days_left_threshold:
                    result.append({
                        "product_id": p["product_id"],
                        "name": p["name"],
                        "quantity": p["quantity"],
                        "sales_velocity": velocity,
                        "days_left": round(days_left, 1)
                    })
        return sorted(result, key=lambda x: x["days_left"])

    # ---------- 4. Overstock Detection ----------
    def get_overstocked_products(self, days=30, stock_threshold=50, sales_threshold=5):
        """Products sitting with a lot of stock but barely selling."""
        totals = self._sales_in_period(days)
        products = self.db.get_products()
        result = []
        for p in products:
            sold = totals.get(p["product_id"], 0)
            if p["quantity"] > stock_threshold and sold < sales_threshold:
                result.append({
                    "product_id": p["product_id"],
                    "name": p["name"],
                    "quantity": p["quantity"],
                    "sales_in_period": sold
                })
        return sorted(result, key=lambda x: x["quantity"], reverse=True)

    # ---------- 5. Restocking Recommendations ----------
    def get_restocking_recommendations(self, days=30, safety_stock=5):
        """For products at/below reorder level, suggest how much to order
        so stock covers roughly the next 30 days of expected sales."""
        products = self.db.get_products()
        result = []
        for p in products:
            if p["quantity"] <= p["reorder_level"]:
                velocity = self._sales_velocity(p["product_id"], days)
                recommended = max(0, (velocity * 30) + safety_stock - p["quantity"])
                if recommended > 0:
                    result.append({
                        "product_id": p["product_id"],
                        "name": p["name"],
                        "quantity": p["quantity"],
                        "reorder_level": p["reorder_level"],
                        "recommended_qty": int(recommended) + 1
                    })
        return sorted(result, key=lambda x: x["quantity"])
