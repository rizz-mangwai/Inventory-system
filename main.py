"""
Smart Electronic Inventory Management System – CLI version.
Uses simple JSON storage, no external dependencies.
"""

import sys
from database.db_manager import DatabaseManager
from services.product_service import ProductService
from services.category_service import CategoryService
from services.supplier_service import SupplierService
from services.customer_service import CustomerService
from services.sales_service import SalesService
from services.inventory_service import InventoryService
from services.ai_assistant import AIAssistant
from utils.helpers import print_header

from menus.product_menu import product_menu
from menus.category_menu import category_menu
from menus.supplier_menu import supplier_menu
from menus.customer_menu import customer_menu
from menus.sales_menu import sales_menu
from menus.inventory_menu import inventory_menu, show_alerts
from menus.reports_menu import reports_menu
from menus.ai_assistant_menu import ai_assistant_menu


def main():
    db = DatabaseManager()
    db.load_data()

    product_service = ProductService(db)
    category_service = CategoryService(db)
    supplier_service = SupplierService(db)
    customer_service = CustomerService(db)
    sales_service = SalesService(db)
    inventory_service = InventoryService(db)
    ai_assistant = AIAssistant(db)

    while True:
        print_header("SMART ELECTRONIC INVENTORY SYSTEM")
        print("1. Product Management")
        print("2. Category Management")
        print("3. Supplier Management")
        print("4. Customer Management")
        print("5. Sales Management")
        print("6. Inventory Management")
        print("7. Stock Alerts")
        print("8. Reports")
        print("9. AI Assistant")
        print("0. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            product_menu(product_service, category_service, supplier_service)
        elif choice == '2':
            category_menu(category_service)
        elif choice == '3':
            supplier_menu(supplier_service)
        elif choice == '4':
            customer_menu(customer_service)
        elif choice == '5':
            sales_menu(sales_service, product_service, customer_service)
        elif choice == '6':
            inventory_menu(inventory_service, product_service)
        elif choice == '7':
            show_alerts(inventory_service)
        elif choice == '8':
            reports_menu(sales_service, inventory_service, ai_assistant)
        elif choice == '9':
            ai_assistant_menu(ai_assistant)
        elif choice == '0':
            print("Exiting... Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()