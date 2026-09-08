class CategoryService:
    def __init__(self, db):
        self.db = db

    def _get_next_id(self):
        categories = self.db.get_categories()
        if not categories:
            return 1
        return max(c["category_id"] for c in categories) + 1

    def add(self, name, description=""):
        categories = self.db.get_categories()
        # Prevent duplicate names
        for c in categories:
            if c["name"].lower() == name.lower():
                return False
        category = {
            "category_id": self._get_next_id(),
            "name": name,
            "description": description
        }
        categories.append(category)
        self.db.set_categories(categories)
        return True

    def get_all(self):
        return self.db.get_categories()

    def get_by_id(self, category_id):
        categories = self.db.get_categories()
        for c in categories:
            if c["category_id"] == category_id:
                return c
        return None

    def update(self, category_id, name, description):
        categories = self.db.get_categories()
        for c in categories:
            if c["category_id"] == category_id:
                c["name"] = name
                c["description"] = description
                self.db.set_categories(categories)
                return True
        return False

    def delete(self, category_id):
        # Don't delete a category still used by a product
        products = self.db.get_products()
        for p in products:
            if p["category_id"] == category_id:
                return False
        categories = self.db.get_categories()
        categories = [c for c in categories if c["category_id"] != category_id]
        self.db.set_categories(categories)
        return True
