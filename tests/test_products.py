"""
Tests for ProductService. Run with: python -m pytest tests/
"""

import os
from database.db_manager import DatabaseManager
from services.product_service import ProductService

TEST_DB = "data/test_products.json"


def make_service():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    db = DatabaseManager(TEST_DB)
    db.load_data()
    return ProductService(db)


def test_add_product():
    ps = make_service()
    pid = ps.add("Test Product", 1, 1, 100, 80, 10, 5, "Test description")
    assert pid is not None

    product = ps.get_by_id(pid)
    assert product is not None
    assert product["name"] == "Test Product"
    assert product["quantity"] == 10
    os.remove(TEST_DB)


def test_search_product():
    ps = make_service()
    ps.add("USB Cable", 1, 1, 200, 100, 15, 5, "1 meter charging cable")
    results = ps.search("cable")
    assert len(results) == 1
    assert results[0]["name"] == "USB Cable"
    os.remove(TEST_DB)


def test_update_product():
    ps = make_service()
    pid = ps.add("Old Name", 1, 1, 100, 80, 10, 5)
    updated = ps.update(pid, name="New Name", quantity=20)
    assert updated is True
    product = ps.get_by_id(pid)
    assert product["name"] == "New Name"
    assert product["quantity"] == 20
    os.remove(TEST_DB)


def test_delete_product():
    ps = make_service()
    pid = ps.add("Deletable", 1, 1, 100, 80, 10, 5)
    deleted = ps.delete(pid)
    assert deleted is True
    assert ps.get_by_id(pid) is None
    os.remove(TEST_DB)
