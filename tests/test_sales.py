"""
Tests for SalesService. Run with: python -m pytest tests/
"""

import os
from database.db_manager import DatabaseManager
from services.product_service import ProductService
from services.sales_service import SalesService

TEST_DB = "data/test_sales.json"


def make_services():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    db = DatabaseManager(TEST_DB)
    db.load_data()
    return ProductService(db), SalesService(db)


def test_record_sale_reduces_stock():
    ps, ss = make_services()
    pid = ps.add("Test Product", 1, 1, 100, 80, 10, 5, "Test")

    sale_id = ss.record_sale(pid, 0, 3, 100, "2026-09-01")
    assert sale_id is not None

    product = ps.get_by_id(pid)
    assert product["quantity"] == 7
    os.remove(TEST_DB)


def test_record_sale_fails_when_out_of_stock():
    ps, ss = make_services()
    pid = ps.add("Limited Stock", 1, 1, 100, 80, 2, 5, "Test")

    sale_id = ss.record_sale(pid, 0, 5, 100, "2026-09-01")
    assert sale_id is None

    product = ps.get_by_id(pid)
    assert product["quantity"] == 2
    os.remove(TEST_DB)


def test_total_sales_value():
    ps, ss = make_services()
    pid = ps.add("Item", 1, 1, 100, 80, 20, 5, "Test")
    ss.record_sale(pid, 0, 2, 100, "2026-09-01")
    ss.record_sale(pid, 0, 3, 100, "2026-09-02")

    total = ss.get_total_sales_value()
    assert total == 500
    os.remove(TEST_DB)
