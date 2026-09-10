

from utils.helpers import input_int, input_non_empty, print_header


def supplier_menu(ss):
    while True:
        print_header("SUPPLIER MANAGEMENT")
        print("1. Add Supplier")
        print("2. View Suppliers")
        print("3. Update Supplier")
        print("4. Delete Supplier")
        print("5. Back")
        choice = input("Enter choice: ").strip()
        if choice == '1':
            name = input_non_empty("Supplier name: ")
            contact = input("Contact info: ").strip()
            if ss.add(name, contact):
                print("Supplier added.")
            else:
                print("Failed.")
        elif choice == '2':
            supps = ss.get_all()
            if not supps:
                print("No suppliers.")
            else:
                for s in supps:
                    print(f"{s['supplier_id']}: {s['name']} - {s['contact_info']}")
        elif choice == '3':
            sid = input_int("Supplier ID to update: ", min_val=1)
            supp = ss.get_by_id(sid)
            if not supp:
                print("Not found.")
                continue
            name = input(f"New name ({supp['name']}): ").strip() or supp['name']
            contact = input(f"New contact ({supp['contact_info']}): ").strip() or supp['contact_info']
            if ss.update(sid, name, contact):
                print("Updated.")
            else:
                print("Update failed.")
        elif choice == '4':
            sid = input_int("Supplier ID to delete: ", min_val=1)
            if ss.delete(sid):
                print("Deleted.")
            else:
                print("Delete failed (maybe has products).")
        elif choice == '5':
            break
        else:
            print("Invalid choice.")
