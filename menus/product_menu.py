

from utils.helpers import input_int, input_non_empty, print_header, print_table


def product_menu(product_service, category_service, supplier_service, role="manager"):
    while True:
        print_header("PRODUCT MANAGEMENT")
        print("1. Add Product          [Manager only]")
        print("2. View All Products")
        print("3. Search Product")
        print("4. Update Product       [Manager only]")
        print("5. Delete Product       [Manager only]")
        print("6. Back to Main")
        choice = input("Enter choice: ").strip()
        if choice in ('1', '4', '5') and role != "manager":
            print("Access denied - Manager only.")
        elif choice == '1':
            add_product(product_service, category_service, supplier_service)
        elif choice == '2':
            view_products(product_service)
        elif choice == '3':
            search_product(product_service)
        elif choice == '4':
            update_product(product_service, category_service, supplier_service)
        elif choice == '5':
            delete_product(product_service)
        elif choice == '6':
            break
        else:
            print("Invalid choice.")


def add_product(ps, cs, ss):
    name = input_non_empty("Product name: ")
    categories = cs.get_all()
    if not categories:
        print("No categories found. Please add a category first.")
        return
    print("Select category:")
    for c in categories:
        print(f"{c['category_id']}. {c['name']}")
    cat_id = input_int("Category ID: ", min_val=1)
    suppliers = ss.get_all()
    if not suppliers:
        print("No suppliers found. Please add a supplier first.")
        return
    print("Select supplier:")
    for s in suppliers:
        print(f"{s['supplier_id']}. {s['name']}")
    sup_id = input_int("Supplier ID: ", min_val=1)
    price = input("Selling price: ").strip()
    price = float(price)
    purchase_price = float(input("Purchase price: ").strip())
    quantity = input_int("Initial quantity: ", min_val=0)
    reorder_level = input_int("Reorder level: ", min_val=0)
    description = input("Description (optional): ").strip()

    product_id = ps.add(name, cat_id, sup_id, price, purchase_price, quantity, reorder_level, description)
    if product_id:
        print(f"Product added successfully with ID: {product_id}")
    else:
        print("Failed to add product.")


def view_products(ps):
    products = ps.get_all()
    if not products:
        print("No products found.")
        return
    headers = ["ID", "Name", "Category", "Supplier", "Price", "Stock", "Reorder", "Description"]
    rows = [[p['product_id'], p['name'], p['category_name'], p['supplier_name'],
             p['price'], p['quantity'], p['reorder_level'], p['description'][:30]]
            for p in products]
    print_table(headers, rows)


def search_product(ps):
    term = input("Enter search term (name or description): ").strip()
    products = ps.search(term)
    if not products:
        print("No products found.")
        return
    for p in products:
        print(f"ID:{p['product_id']} | {p['name']} | Stock:{p['quantity']} | Price:{p['price']}")


def update_product(ps, cs, ss):
    pid = input_int("Product ID to update: ", min_val=1)
    product = ps.get_by_id(pid)
    if not product:
        print("Product not found.")
        return
    print("Leave blank to keep current value.")
    name = input(f"Name ({product['name']}): ").strip() or product['name']
    categories = cs.get_all()
    print("Current category:", product.get('category_name', 'Unknown'))
    for c in categories:
        print(f"{c['category_id']}. {c['name']}")
    cat_id = input(f"Category ID ({product['category_id']}): ").strip()
    cat_id = int(cat_id) if cat_id else product['category_id']
    suppliers = ss.get_all()
    print("Current supplier:", product.get('supplier_name', 'Unknown'))
    for s in suppliers:
        print(f"{s['supplier_id']}. {s['name']}")
    sup_id = input(f"Supplier ID ({product['supplier_id']}): ").strip()
    sup_id = int(sup_id) if sup_id else product['supplier_id']
    price = input(f"Selling price ({product['price']}): ").strip()
    price = float(price) if price else product['price']
    purchase_price = input(f"Purchase price ({product['purchase_price']}): ").strip()
    purchase_price = float(purchase_price) if purchase_price else product['purchase_price']
    quantity = input(f"Quantity ({product['quantity']}): ").strip()
    quantity = int(quantity) if quantity else product['quantity']
    reorder_level = input(f"Reorder level ({product['reorder_level']}): ").strip()
    reorder_level = int(reorder_level) if reorder_level else product['reorder_level']
    description = input(f"Description ({product['description']}): ").strip() or product['description']

    if ps.update(pid, name=name, category_id=cat_id, supplier_id=sup_id, price=price,
                 purchase_price=purchase_price, quantity=quantity, reorder_level=reorder_level,
                 description=description):
        print("Product updated.")
    else:
        print("Update failed.")


def delete_product(ps):
    pid = input_int("Product ID to delete: ", min_val=1)
    if ps.delete(pid):
        print("Product deleted.")
    else:
        print("Deletion failed (check if product has sales).")
