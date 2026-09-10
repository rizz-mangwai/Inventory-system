class SupplierService:
    def __init__(self, db):
        self.db = db

    def _get_next_id(self):
        suppliers = self.db.get_suppliers()
        if not suppliers:
            return 1
        return max(s["supplier_id"] for s in suppliers) + 1

    def add(self, name, contact_info=""):
        supplier = {
            "supplier_id": self._get_next_id(),
            "name": name,
            "contact_info": contact_info
        }
        suppliers = self.db.get_suppliers()
        suppliers.append(supplier)
        self.db.set_suppliers(suppliers)
        return True

    def get_all(self):
        return self.db.get_suppliers()

    def get_by_id(self, supplier_id):
        suppliers = self.db.get_suppliers()
        for s in suppliers:
            if s["supplier_id"] == supplier_id:
                return s
        return None

    def update(self, supplier_id, name, contact_info):
        suppliers = self.db.get_suppliers()
        for s in suppliers:
            if s["supplier_id"] == supplier_id:
                s["name"] = name
                s["contact_info"] = contact_info
                self.db.set_suppliers(suppliers)
                return True
        return False

    def delete(self, supplier_id):
        # Don't delete a supplier still used by a product
        products = self.db.get_products()
        for p in products:
            if p["supplier_id"] == supplier_id:
                return False
        suppliers = self.db.get_suppliers()
        suppliers = [s for s in suppliers if s["supplier_id"] != supplier_id]
        self.db.set_suppliers(suppliers)
        return True
