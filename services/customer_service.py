class CustomerService:
    def __init__(self, db):
        self.db = db

    def _get_next_id(self):
        customers = self.db.get_customers()
        if not customers:
            return 1
        return max(c["customer_id"] for c in customers) + 1

    def add(self, name, contact_info=""):
        customer = {
            "customer_id": self._get_next_id(),
            "name": name,
            "contact_info": contact_info
        }
        customers = self.db.get_customers()
        customers.append(customer)
        self.db.set_customers(customers)
        return True

    def get_all(self):
        return self.db.get_customers()

    def get_by_id(self, customer_id):
        customers = self.db.get_customers()
        for c in customers:
            if c["customer_id"] == customer_id:
                return c
        return None

    def update(self, customer_id, name, contact_info):
        customers = self.db.get_customers()
        for c in customers:
            if c["customer_id"] == customer_id:
                c["name"] = name
                c["contact_info"] = contact_info
                self.db.set_customers(customers)
                return True
        return False

    def delete(self, customer_id):
        # Don't delete a customer who already has sales history
        sales = self.db.get_sales()
        for s in sales:
            if s["customer_id"] == customer_id:
                return False
        customers = self.db.get_customers()
        customers = [c for c in customers if c["customer_id"] != customer_id]
        self.db.set_customers(customers)
        return True
