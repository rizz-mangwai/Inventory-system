"""
Adds a full set of electronics categories to your EXISTING data —
safe to run even if you already have products/sales saved.
Won't create duplicates if a category name already exists.

Run with: python add_electronics_categories.py
"""

from database.db_manager import DatabaseManager
from services.category_service import CategoryService

ELECTRONICS_CATEGORIES = [
    ("Phones", "Smartphones and accessories"),
    ("Audio", "Headphones and speakers"),
    ("Computing", "Laptops and peripherals"),
    ("Televisions", "Smart TVs and TV accessories"),
    ("Home Appliances", "Fridges, microwaves, blenders, irons"),
    ("Cameras", "Digital cameras and photography gear"),
    ("Gaming", "Consoles, controllers, and gaming accessories"),
    ("Wearables", "Smartwatches and fitness trackers"),
    ("Networking", "Routers, modems, and network cables"),
    ("Power & Charging", "Chargers, power banks, batteries, cables"),
    ("Accessories", "Cases, stands, and general electronic accessories"),
]


def main():
    db = DatabaseManager()
    db.load_data()
    cs = CategoryService(db)

    added = 0
    skipped = 0
    for name, description in ELECTRONICS_CATEGORIES:
        if cs.add(name, description):
            added += 1
        else:
            skipped += 1

    print(f"Added {added} new categories. Skipped {skipped} that already existed.")
    print("\nAll categories now:")
    for c in cs.get_all():
        print(f"  {c['category_id']}. {c['name']}")


if __name__ == "__main__":
    main()