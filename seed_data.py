"""
Populates data/inventory.json with sample categories, suppliers,
products, and a few weeks of sales history — so the AI Assistant has
something real to analyze right after setup.

Run once with: python seed_sample_data.py
"""

from datetime import datetime, timedelta
from database.db_manager import DatabaseManager
from services.category_service import CategoryService
from services.supplier_service import SupplierService
from services.customer_service import CustomerService
from services.product_service import ProductService
from services.sales_service import SalesService


def days_ago(n):
    return (datetime.now() - timedelta(days=n)).strftime("%Y-%m-%d")


def main():
    db = DatabaseManager()
    db.load_data()

    cs = CategoryService(db)
    ss = SupplierService(db)
    cus = CustomerService(db)
    ps = ProductService(db)
    sales = SalesService(db)

    cs.add("Phones", "Smartphones and accessories")
    cs.add("Audio", "Headphones and speakers")
    cs.add("Computing", "Laptops and peripherals")
    cs.add("Televisions", "Smart TVs and TV accessories")
    cs.add("Home Appliances", "Fridges, microwaves, blenders, irons")
    cs.add("Cameras", "Digital cameras and photography gear")
    cs.add("Gaming", "Consoles, controllers, and gaming accessories")
    cs.add("Wearables", "Smartwatches and fitness trackers")
    cs.add("Networking", "Routers, modems, and network cables")
    cs.add("Power & Charging", "Chargers, power banks, batteries, cables")
    cs.add("Accessories", "Cases, stands, and general electronic accessories")

    ss.add("TechDistributors Ltd", "sales@techdist.co.ke")
    ss.add("Nairobi Electronics Wholesale", "orders@nbowholesale.co.ke")

    cus.add("Walk-in Customer", "")
    cus.add("Amina Retail Shop", "amina.shop@example.com")

    categories = cs.get_all()
    suppliers = ss.get_all()
    phones_id = categories[0]["category_id"]
    audio_id = categories[1]["category_id"]
    computing_id = categories[2]["category_id"]
    sup1 = suppliers[0]["supplier_id"]
    sup2 = suppliers[1]["supplier_id"]

    # name, category, supplier, price, cost, stock, reorder_level
    p1 = ps.add("USB-C Fast Charger 33W", phones_id, sup1, 1500, 900, 40, 10)
    p2 = ps.add("Wireless Earbuds Pro", audio_id, sup2, 3500, 2200, 60, 15)
    p3 = ps.add("Bluetooth Speaker Mini", audio_id, sup2, 2800, 1700, 8, 10)
    p4 = ps.add("HDMI Cable 2m", computing_id, sup1, 700, 350, 90, 20)
    p5 = ps.add("Laptop Cooling Pad", computing_id, sup1, 2200, 1400, 55, 10)
    p6 = ps.add("Screen Protector Glass", phones_id, sup1, 300, 120, 120, 30)

    # Fast movers
    for i in range(1, 21):
        sales.record_sale(p1, 1, 3, 1600, days_ago(i))
    for i in range(1, 16):
        sales.record_sale(p2, 2, 4, 3700, days_ago(i))

    # Slow mover
    sales.record_sale(p3, 1, 1, 2900, days_ago(25))

    # Overstocked
    sales.record_sale(p4, 1, 2, 750, days_ago(20))
    sales.record_sale(p6, 1, 3, 320, days_ago(18))

    # Moderate seller
    for i in range(3, 30, 5):
        sales.record_sale(p5, 2, 2, 2400, days_ago(i))

    print("Sample data created in data/inventory.json")
    print(f"Products: {len(ps.get_all())} | Sales recorded: {len(sales.get_all())}")


if __name__ == "__main__":
    main()