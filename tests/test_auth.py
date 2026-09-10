

import os
from database.db_manager import DatabaseManager
from services.auth_service import AuthService

TEST_DB = "data/test_auth.json"


def make_service():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    db = DatabaseManager(TEST_DB)
    db.load_data()
    return AuthService(db)


def test_default_accounts_are_seeded():
    auth = make_service()
    users = auth.get_all()
    usernames = [u["username"] for u in users]
    assert "admin" in usernames
    assert "staff" in usernames
    os.remove(TEST_DB)


def test_login_with_correct_credentials():
    auth = make_service()
    user = auth.login("admin", "admin123")
    assert user is not None
    assert user["role"] == "manager"
    os.remove(TEST_DB)


def test_login_with_wrong_password_fails():
    auth = make_service()
    user = auth.login("admin", "wrongpassword")
    assert user is None
    os.remove(TEST_DB)


def test_add_new_user():
    auth = make_service()
    added = auth.add_user("jane", "jane123", "employee")
    assert added is True

    user = auth.login("jane", "jane123")
    assert user is not None
    assert user["role"] == "employee"
    os.remove(TEST_DB)


def test_cannot_add_duplicate_username():
    auth = make_service()
    auth.add_user("jane", "jane123", "employee")
    duplicate = auth.add_user("jane", "differentpassword", "manager")
    assert duplicate is False
    os.remove(TEST_DB)
