

from utils.helpers import print_header

def reports_menu(sales_service, inventory_service, ai_assistant):
    while True:
        print_header("REPORTS")
        print("1. Total Sales Value")
        print("2. Sales by Product")
        print("3. Inventory Value")
        print("4. Product Movement (Fast/Slow)")
        print("5. Back")
        choice = input("Enter choice: ").strip()
        if choice == '1':
            total = sales_service.get_total_sales_value()
            print(f"Total Sales Value: ${total:.2f}")
        elif choice == '2':
            report = sales_service.get_sales_by_product()
            if not report:
                print("No sales data.")
            else:
                for r in report:
                    print(f"{r['product_name']}: {r['total_qty']} units, ${r['total_value']:.2f}")
        elif choice == '3':
            value = inventory_service.get_total_inventory_value()
            print(f"Total Inventory Value: ${value:.2f}")
        elif choice == '4':
            fast = ai_assistant.get_fast_moving_products(days=30, min_sales=5)
            slow = ai_assistant.get_slow_moving_products(days=30, max_sales=1)
            print("Fast-moving products (sales >= 5 units in 30 days):")
            for p in fast:
                print(f"  {p['name']} - {p['sales_velocity']:.2f} units/day")
            print("Slow-moving products (sales <= 1 unit in 30 days):")
            for p in slow:
                print(f"  {p['name']} - {p['sales_velocity']:.2f} units/day")
        elif choice == '5':
            break
        else:
            print("Invalid choice.")
