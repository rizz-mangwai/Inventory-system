

from utils.helpers import input_int, print_header, print_table


def inventory_menu(inv_service, prod_service):
    while True:
        print_header("INVENTORY MANAGEMENT")
        print("1. View Current Inventory")
        print("2. Update Stock (Restock)")
        print("3. View Low Stock Products")
        print("4. Back")
        choice = input("Enter choice: ").strip()
        if choice == '1':
            view_inventory(inv_service)
        elif choice == '2':
            restock(inv_service, prod_service)
        elif choice == '3':
            low_stock = inv_service.get_low_stock()
            if not low_stock:
                print("No low stock products.")
            else:
                for p in low_stock:
                    print(f"{p['name']} - Current: {p['quantity']}, Reorder: {p['reorder_level']}")
        elif choice == '4':
            break
        else:
            print("Invalid choice.")


def view_inventory(inv_service):
    inv = inv_service.get_all_with_product()
    if not inv:
        print("No inventory records.")
        return
    headers = ["Product ID", "Name", "Stock", "Last Updated"]
    rows = [[i['product_id'], i['product_name'], i['quantity_in_stock'], i['last_updated']] for i in inv]
    print_table(headers, rows)


def restock(inv_service, prod_service):
    pid = input_int("Product ID to restock: ", min_val=1)
    product = prod_service.get_by_id(pid)
    if not product:
        print("Product not found.")
        return
    qty = input_int("Quantity to add: ", min_val=1)
    if inv_service.update_stock(pid, qty, operation='add'):
        print("Stock updated.")
    else:
        print("Update failed.")


def show_alerts(inv_service):
    print_header("STOCK ALERTS")
    alerts = inv_service.get_low_stock()
    if not alerts:
        print("All products are above reorder level.")
    else:
        print("The following products are low on stock:")
        for p in alerts:
            print(f"- {p['name']}: {p['quantity']} units (reorder level: {p['reorder_level']})")
