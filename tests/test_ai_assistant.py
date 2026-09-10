

import os
from datetime import datetime, timedelta
from database.db_manager import DatabaseManager
from services.product_service import ProductService
from services.sales_service import SalesService
from services.ai_assistant import AIAssistant

TEST_DB = "data/test_ai_assistant.json"


def days_ago(n):
    return (datetime.now() - timedelta(days=n)).strftime("%Y-%m-%d")


def make_services():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    db = DatabaseManager(TEST_DB)
    db.load_data()
    return ProductService(db), SalesService(db), AIAssistant(db)


def test_fast_moving_products():
    ps, ss, ai = make_services()
    fast_id = ps.add("Fast Seller", 1, 1, 100, 50, 100, 10, "")
    ss.record_sale(fast_id, 0, 3, 100, days_ago(5))
    ss.record_sale(fast_id, 0, 4, 100, days_ago(10))

    fast = ai.get_fast_moving_products(days=30, min_sales=5)
    assert len(fast) == 1
    assert fast[0]["name"] == "Fast Seller"
    os.remove(TEST_DB)


def test_slow_moving_products():
    ps, ss, ai = make_services()
    slow_id = ps.add("Slow Seller", 1, 1, 100, 50, 100, 10, "")
    ss.record_sale(slow_id, 0, 1, 100, days_ago(20))

    slow = ai.get_slow_moving_products(days=30, max_sales=1)
    assert len(slow) == 1
    assert slow[0]["name"] == "Slow Seller"
    os.remove(TEST_DB)


def test_stockout_risk():
    ps, ss, ai = make_services()
    # Sells 2/day, only 4 left in stock -> 2 days of stock left
    risky_id = ps.add("Risky Product", 1, 1, 100, 50, 4, 10, "")
    for i in range(1, 11):
        ss.record_sale(risky_id, 0, 2, 100, days_ago(i))

    risk = ai.get_stockout_risk(days=30)
    assert len(risk) == 1
    assert risk[0]["name"] == "Risky Product"
    assert risk[0]["days_left"] < 5
    os.remove(TEST_DB)


def test_overstocked_products():
    ps, ss, ai = make_services()
    over_id = ps.add("Overstocked Item", 1, 1, 100, 50, 200, 10, "")
    ss.record_sale(over_id, 0, 1, 100, days_ago(15))

    overstock = ai.get_overstocked_products(days=30, stock_threshold=50, sales_threshold=5)
    assert len(overstock) == 1
    assert overstock[0]["name"] == "Overstocked Item"
    os.remove(TEST_DB)


def test_restocking_recommendations():
    ps, ss, ai = make_services()
    # Below reorder level, with a sales history to base a recommendation on
    low_id = ps.add("Needs Restock", 1, 1, 100, 50, 3, 10, "")
    for i in range(1, 6):
        ss.record_sale(low_id, 0, 2, 100, days_ago(i))

    recs = ai.get_restocking_recommendations(days=30)
    assert len(recs) == 1
    assert recs[0]["name"] == "Needs Restock"
    assert recs[0]["recommended_qty"] > 0
    os.remove(TEST_DB)
