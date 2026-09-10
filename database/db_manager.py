"""
Simple JSON-based storage 
keeps everything in one file: data/inventory.json
"""
import json
import os

EMPTY_DATA = {
    "products": [],
    "categories": [],
    "suppliers": [],
    "customers": [],
    "sales": [],
    "inventory": [],
    "users": [],
}


class DatabaseManager:
    def __init__(self, db_path="data/inventory.json"):
        self.db_path = db_path
        self.data = dict(EMPTY_DATA)
        self.load_data()

 
    def load_data(self):
        """load sata from JSON file, or create empty structure."""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r") as f:
                    self.data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.data = dict(EMPTY_DATA)
                self.save_data()


        else:
            folder = os.path.dirname(self.db_path)
            if folder: 
                os.makedirs(folder, exist_ok=True)
            self.save_data()



    def save_data(self):
        """save all data to JSON file."""
        with open(self.db_path, "w") as f:
            json.dump(self.data, f, indent=4)


    def get_products(self):
        return self.data["products"]


    def set_products(self, products):
        self.data["products"] = products
        self.save_data()

    def get_categories(self):
        return self.data["categories"]


    def set_categories(self, categories):
        self.data["categories"] = categories
        self.save_data()


    def get_suppliers(self):
        return self.data["suppliers"]

    def set_suppliers(self, suppliers):
        self.data["suppliers"] = suppliers
        self.save_data()

    def get_customers(self):
        return self.data["customers"]

    def set_customers(self, customers):
        self.data["customers"] = customers
        self.save_data()

    def get_sales(self):
        return self.data["sales"]

    def set_sales(self, sales):
        self.data["sales"] = sales
        self.save_data()

    def get_inventory(self):
        return self.data["inventory"]

    def set_inventory(self, inventory):
        self.data["inventory"] = inventory
        self.save_data()   

    def get_users(self):
        return self.data.get("users", [])

    def set_users(self, users):
        self.data["users"] = users
        self.save_data()    


