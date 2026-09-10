from utils.helpers import input_int, input_float, input_date, print_header, print_table


def sales_menu(sales_service, product_service, customer_service):
    while True:
        print_header("SALES MANAGEMENT")
        print("1. Record Sale")
        print("2. View All Sales")
        print("3. View Sales by Product")
        print("4. View Sales by Customer")
        print("5. Back")
        choice = input("Enter choice: ").strip()
        if choice == '1':
            record_sale(sales_service, product_service, customer_service)
        elif choice == '2':
            view_sales(sales_service)
        elif choice == '3':
            pid = input_int("Product ID: ", min_val=1)
            sales = sales_service.get_by_product(pid)
            if not sales:
                print("No sales for this product.")
            else:
                for s in sales:
                    print(f"Sale {s['sale_id']}: Qty={s['quantity']}, Price={s['sale_price']}, Date={s['date']}, Customer={s['customer_name']}")
        elif choice == '4':
            cid = input_int("Customer ID: ", min_val=1)
            sales = sales_service.get_by_customer(cid)
            if not sales:
                print("No sales for this customer.")
            else:
                for s in sales:
                    print(f"Sale {s['sale_id']}: Product={s['product_name']}, Qty={s['quantity']}, Date={s['date']}")
        elif choice == '5':
            break
        else:
            print("Invalid choice.")


def record_sale(ss, ps, cs):
    product_id = input_int("Product ID: ", min_val=1)
    product = ps.get_by_id(product_id)
    if not product:
        print("Product not found.")
        return
    print(f"Current stock: {product['quantity']}")
    qty = input_int("Quantity sold: ", min_val=1)
    if qty > product['quantity']:
        print("Not enough stock.")
        return
    customer_id = input_int("Customer ID (0 if none): ", min_val=0)
    if customer_id != 0:
        cust = cs.get_by_id(customer_id)
        if not cust:
            print("Customer not found.")
            return
    sale_price = input_float("Sale price per unit: ", min_val=0)
    date = input_date("Sale date (YYYY-MM-DD) [today]: ") or None

    sale_id = ss.record_sale(product_id, customer_id, qty, sale_price, date)
    if sale_id:
        print(f"Sale recorded with ID: {sale_id}. Stock updated.")
    else:
        print("Sale failed.")


def view_sales(ss):
    sales = ss.get_all()
    if not sales:
        print("No sales.")
        return
    headers = ["ID", "Product", "Customer", "Qty", "Unit Price", "Total", "Date"]
    rows = [[s['sale_id'], s['product_name'], s['customer_name'], s['quantity'],
             s['sale_price'], s['quantity']*s['sale_price'], s['date']] for s in sales]
    print_table(headers, rows)