from utils.helpers import input_int, input_non_empty, print_header


def category_menu(cs):
    while True:
        print_header("CATEGORY MANAGEMENT")
        print("1. Add Category")
        print("2. View Categories")
        print("3. Update Category")
        print("4. Delete Category")
        print("5. Back")
        choice = input("Enter choice: ").strip()
        if choice == '1':
            name = input_non_empty("Category name: ")
            desc = input("Description: ").strip()
            if cs.add(name, desc):
                print("Category added.")
            else:
                print("Failed (maybe duplicate name).")
        elif choice == '2':
            cats = cs.get_all()
            if not cats:
                print("No categories.")
            else:
                for c in cats:
                    print(f"{c['category_id']}: {c['name']} - {c['description']}")
        elif choice == '3':
            cid = input_int("Category ID to update: ", min_val=1)
            cat = cs.get_by_id(cid)
            if not cat:
                print("Not found.")
                continue
            name = input(f"New name ({cat['name']}): ").strip() or cat['name']
            desc = input(f"New description ({cat['description']}): ").strip() or cat['description']
            if cs.update(cid, name, desc):
                print("Updated.")
            else:
                print("Update failed.")
        elif choice == '4':
            cid = input_int("Category ID to delete: ", min_val=1)
            if cs.delete(cid):
                print("Deleted.")
            else:
                print("Delete failed (maybe has products).")
        elif choice == '5':
            break
        else:
            print("Invalid choice.")