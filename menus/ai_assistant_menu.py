

from utils.helpers import input_int, print_header


def ai_assistant_menu(service):
    while True:
        print_header("AI INVENTORY ASSISTANT")
        print("1. Fast-Moving Products")
        print("2. Slow-Moving Products")
        print("3. Stockout Risk")
        print("4. Overstock Detection")
        print("5. Restocking Recommendations")
        print("6. Back")
        choice = input("Enter choice: ").strip()

        if choice == '1':
            days = input_int("Lookback days (e.g., 30): ", min_val=1, default=30)
            threshold = input_int("Minimum sales units to consider fast: ", min_val=1, default=5)
            fast = service.get_fast_moving_products(days, threshold)
            if not fast:
                print("No fast-moving products found.")
            else:
                print("\nFast-Moving Products:")
                for p in fast:
                    print(f"  {p['name']} - {p['sales_velocity']:.2f} units/day "
                          f"({p['total_sold_period']} sold in last {days} days)")

        elif choice == '2':
            days = input_int("Lookback days: ", min_val=1, default=30)
            threshold = input_int("Maximum sales units to consider slow: ", min_val=0, default=1)
            slow = service.get_slow_moving_products(days, threshold)
            if not slow:
                print("No slow-moving products found.")
            else:
                print("\nSlow-Moving Products:")
                for p in slow:
                    print(f"  {p['name']} - {p['sales_velocity']:.2f} units/day "
                          f"({p['total_sold_period']} sold in last {days} days)")

        elif choice == '3':
            days = input_int("Lookback days for sales velocity: ", min_val=1, default=30)
            risk = service.get_stockout_risk(days)
            if not risk:
                print("No products at risk of stockout.")
            else:
                print("\nStockout Risk:")
                for p in risk:
                    print(f"  {p['name']} - Stock: {p['quantity']}, "
                          f"Days left: {p['days_left']:.1f}")

        elif choice == '4':
            days = input_int("Lookback days: ", min_val=1, default=30)
            overstock = service.get_overstocked_products(days)
            if not overstock:
                print("No overstocked products detected.")
            else:
                print("\nOverstocked Products:")
                for p in overstock:
                    print(f"  {p['name']} - Stock: {p['quantity']}, "
                          f"Sales: {p['sales_in_period']} units")

        elif choice == '5':
            days = input_int("Lookback days: ", min_val=1, default=30)
            recs = service.get_restocking_recommendations(days)
            if not recs:
                print("No recommendations at this time.")
            else:
                print("\nRestocking Recommendations:")
                for r in recs:
                    print(f"  {r['name']} - Current: {r['quantity']}, Reorder level: {r['reorder_level']}, "
                          f"Recommended order: {r['recommended_qty']}")

        elif choice == '6':
            break
        else:
            print("Invalid choice.")
