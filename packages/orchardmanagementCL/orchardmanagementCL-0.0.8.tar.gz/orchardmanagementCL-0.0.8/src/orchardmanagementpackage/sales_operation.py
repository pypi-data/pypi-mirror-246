from src.orchardmanagementpackage.management.inventory import InventoryManagement
from src.orchardmanagementpackage.management.sales import SalesManagement


def sales_operator(extra_productivity_file, remaining_productivity_file, inventory_file, order_file):
    # Instantiate the InventoryManagement class
    inventory_manager = InventoryManagement(extra_productivity_file, remaining_productivity_file, inventory_file)

    # Instantiate the SalesManagement class with the inventory manager
    sales_manager = SalesManagement(inventory_manager, order_file)

    while True:
        print("Sales Operations:")
        print("1. Add Sales Order")
        print("2. Add Picking Order")
        print("3. Display Orders")
        print("4. Display Revenue by Sales Type or Fruit Type")
        print("5. Plot Revenue Distribution by Fruit Type")
        print("0. Back to Main Menu")

        operation_choice = input("Please enter operation index here: ")

        try:
            operation_choice = int(operation_choice)
            if operation_choice == 1:
                fruit_variety = input("Enter fruit variety(choose from Ambrosia, Lapins, Elberta): ")
                weight = float(input("Enter weight: "))
                sales_manager.check_inventory(fruit_variety, weight)
                sales_manager.add_order("selling", fruit_variety, weight)
            elif operation_choice == 2:
                fruit_variety = input("Enter fruit variety(choose from Ambrosia, Lapins, Elberta): ")
                weight = float(input("Enter weight: "))
                sales_manager.add_order("picking", fruit_variety, weight)
                print("saving successfully")
            elif operation_choice == 3:
                sales_manager.order_display()
            elif operation_choice == 4:
                variable = input("Enter variable (sales_type or fruit_type): ")
                sales_manager.revenue_display(variable)
            elif operation_choice == 5:
                sales_manager.revenue_plotter()
            elif operation_choice == 0:
                print("Back to the Main Menu.")
                break
            else:
                print("Invalid operation index.")
        except ValueError:
            print("Invalid input, please enter operation index.")
