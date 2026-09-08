"""
Auth service – handles login and user roles (manager / employee).

Note for a real production app: passwords would be hashed, not stored
as plain text. For this school project, plain text keeps the code
simple to read and understand, but it would NOT be safe to use for a
real shop's actual staff logins.
"""


class AuthService:
    def __init__(self, db):
        self.db = db
        self._seed_default_users()

    def _seed_default_users(self):
        """Create two starter accounts the first time the app ever runs,
        so there's always a way to log in."""
        users = self.db.get_users()
        if not users:
            users = [
                {"username": "admin", "password": "admin123", "role": "manager"},
                {"username": "staff", "password": "staff123", "role": "employee"},
            ]
            self.db.set_users(users)

    def login(self, username, password):
        """Return the matching user dict if username+password are correct,
        otherwise None."""
        users = self.db.get_users()
        for u in users:
            if u["username"] == username and u["password"] == password:
                return u
        return None

    def add_user(self, username, password, role):
        """role must be 'manager' or 'employee'. Returns False if the
        username is already taken."""
        users = self.db.get_users()
        for u in users:
            if u["username"].lower() == username.lower():
                return False
        users.append({"username": username, "password": password, "role": role})
        self.db.set_users(users)
        return True

    def get_all(self):
        return self.db.get_users()
