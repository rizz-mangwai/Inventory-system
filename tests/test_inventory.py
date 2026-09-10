"""
Tests for InventoryService. Run with: python -m pytest tests/
"""

import os
from database.db_manager import DatabaseManager
from services.product_service import ProductService
from services.inventory_service import InventoryService

TEST_DB = "data/test_inventory.json"


def make_services():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    db = DatabaseManager(TEST_DB)
    db.load_data()
    return ProductService(db), InventoryService(db)


def test_update_stock_add():
    ps, inv = make_services()
    pid = ps.add("Widget", 1, 1, 100, 80, 10, 5, "Test")

    updated = inv.update_stock(pid, 5, operation="add")
    assert updated is True
    product = ps.get_by_id(pid)
    assert product["quantity"] == 15
    os.remove(TEST_DB)


def test_get_low_stock():
    ps, inv = make_services()
    ps.add("Low Item", 1, 1, 100, 80, 2, 10, "Below reorder level")
    ps.add("Healthy Item", 1, 1, 100, 80, 50, 10, "Well stocked")

    low = inv.get_low_stock()
    assert len(low) == 1
    assert low[0]["name"] == "Low Item"
    os.remove(TEST_DB)


def test_total_inventory_value():
    ps, inv = make_services()
    ps.add("Item A", 1, 1, 100, 50, 10, 5)
    ps.add("Item B", 1, 1, 200, 100, 5, 5)

    # (10 * 50) + (5 * 100) = 500 + 500 = 1000
    assert inv.get_total_inventory_value() == 1000
    os.remove(TEST_DB)
