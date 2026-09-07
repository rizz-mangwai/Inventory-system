

from utils.helpers import input_int, input_non_empty, print_header

def customer_menu(cs):
    while True:
        print_header("CUSTOMER MANAGEMENT")
        print("1. Add Customer")
        print("2. View Customers")
        print("3. Update Customer")
        print("4. Delete Customer")
        print("5. Back")
        choice = input("Enter choice: ").strip()
        if choice == '1':
            name = input_non_empty("Customer name: ")
            contact = input("Contact info: ").strip()
            if cs.add(name, contact):
                print("Customer added.")
            else:
                print("Failed.")
        elif choice == '2':
            custs = cs.get_all()
            if not custs:
                print("No customers.")
            else:
                for c in custs:
                    print(f"{c['customer_id']}: {c['name']} - {c['contact_info']}")
        elif choice == '3':
            cid = input_int("Customer ID to update: ", min_val=1)
            cust = cs.get_by_id(cid)
            if not cust:
                print("Not found.")
                continue
            name = input(f"New name ({cust['name']}): ").strip() or cust['name']
            contact = input(f"New contact ({cust['contact_info']}): ").strip() or cust['contact_info']
            if cs.update(cid, name, contact):
                print("Updated.")
            else:
                print("Update failed.")
        elif choice == '4':
            cid = input_int("Customer ID to delete: ", min_val=1)
            if cs.delete(cid):
                print("Deleted.")
            else:
                print("Delete failed (maybe has sales).")
        elif choice == '5':
            break
        else:
            print("Invalid choice.")
