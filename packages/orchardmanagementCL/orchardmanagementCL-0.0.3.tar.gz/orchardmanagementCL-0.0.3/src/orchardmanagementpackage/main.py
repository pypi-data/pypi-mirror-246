import os
import sys
from io import StringIO
import pandas as pd
import src.orchardmanagementpackage.production.fruit_info as fruit_info
import src.orchardmanagementpackage.production.plantation as plantation
import src.orchardmanagementpackage.management.inventory as inventory
import src.orchardmanagementpackage.management.sales as sales
import src.orchardmanagementpackage.fruit_info_operation as fruit_info_operation
import src.orchardmanagementpackage.plantation_operation as plantation_operation
import src.orchardmanagementpackage.inventory_operation as inventory_operation
import src.orchardmanagementpackage.sales_operation as sales_operation


def basic_choice_select(fruit_file, plantation_file, extra_productivity_file, remaining_productivity_file,
                        inventory_file, order_file):
    """
    Interact contents
    """
    while True:
        print("1. View and manage fruit categories in the orchard.")
        print("2. View and manage production regions in the orchard")
        print("3. Manage or visualize inventory of the orchard")
        print("4. Manage or visualize sales of the orchard")
        print("0. exit the system")

        choice_input = input("Please enter your choice: ")
        try:
            choice_input = int(choice_input)
            if choice_input == 1:
                fruit_info_operation.fruits_operations(fruit_file)
            elif choice_input == 2:
                plantation_operation.region_operations(fruit_file, plantation_file)

            elif choice_input == 3:
                inventory_operation.inventory_operator(extra_productivity_file, remaining_productivity_file,
                                                       inventory_file)
            elif choice_input == 4:
                sales_operation.sales_operator(extra_productivity_file, remaining_productivity_file, inventory_file, order_file)
            elif choice_input == 0:
                sys.exit()
            else:
                print("Invalid input, please enter a valid choice.")
        except ValueError:
            print("Invalid input, please enter the number of your choice.")


def file_import(relative_path):
    """
    Create absolute path
    """
    current_directory = os.getcwd()
    fruit_file = os.path.join(current_directory, relative_path)
    return fruit_file


def clear_csv_file(file_path):
    """
    Initialize files
    """
    # Read the CSV file, keeping only the column names
    df = pd.read_csv(file_path, nrows=0)
    # Overwrite the file, writing only the column names
    df.to_csv(file_path, index=False)


def fruit_init(fruit_file):
    '''
    Initialize fruit_information
    '''
    df = pd.DataFrame()
    df.to_csv(fruit_file, index=False)
    fruit_info.add_fruit(1, "Ambrosia", "big", "very sweet",
                         "less sour", "crunchy", 1.2, "pie", fruit_file)
    fruit_info.add_fruit(3, "Elberta", "big", "very sweet",
                         "less sour", "crunchy", 1.2, "pie", fruit_file)
    fruit_info.add_fruit(2, "Lapins", "small", "median sweet",
                         "median sour", "soft", 2.99, "cans", fruit_file)

def plantation_init(fruit_file, plantation_file):

    '''
    Initialize plantation information
    '''
    clear_csv_file(plantation_file)
    fruit_list = fruit_info.fruit_class_load(fruit_file)
    try:
        plantation.add_region(1, 1, "Ambrosia", 20, "market",
                              fruit_list, plantation_file)
        plantation.add_region(2, 3, "Elberta", 30, "market",
                              fruit_list, plantation_file)
        plantation.add_region(3, 2, "Lapins", 40, "pick",
                              fruit_list, plantation_file)
        plantation.add_region(4, 2, "Lapins", 40, "pick",
                              fruit_list, plantation_file)
    except plantation.FruitNoneException as e:
        print(f"Fail to add region, {e}")
    except plantation.RegionExistException as r:
        print(f"Fail to add region, {r}")



def inventory_init(extra_productivity_file, remaining_productivity_file, inventory_file):
    """
    Initialize inventory module
    """
    original_stdout = sys.stdout
    sys.stdout = StringIO()
    clear_csv_file(inventory_file)
    clear_csv_file(remaining_productivity_file)
    clear_csv_file(extra_productivity_file)
    inventory_manager = inventory.InventoryManagement(extra_productivity_file, remaining_productivity_file,
                                                      inventory_file)
    inventory_manager.total_product_estimate()
    inventory_manager.add_inventory('Ambrosia', 300)
    inventory_manager.add_inventory("Honeycrisp", 300)
    inventory_manager.add_inventory("Gala", 300)
    inventory_manager.add_inventory('Elberta', 400)
    inventory_manager.add_inventory('Lapins', 500)
    sys.stdout = original_stdout


def sales_init(extra_productivity_file, remaining_productivity_file, inventory_file, order_file):
    """
    Initialize sales module
    """
    original_stdout = sys.stdout
    sys.stdout = StringIO()
    inventory_manager = inventory.InventoryManagement(extra_productivity_file, remaining_productivity_file,
                                                      inventory_file, )
    clear_csv_file(order_file)
    # Instantiate the SalesManagement class with the inventory manager
    sales_manager = sales.SalesManagement(inventory_manager, order_file)
    # Add some orders
    sales_manager.add_order('selling', 'Ambrosia', 50)
    sales_manager.add_order('selling', 'Elberta', 50)
    sales_manager.add_order('picking', 'Lapins', 40)
    sys.stdout = original_stdout


if __name__ == '__main__':
    print("Welcome to the Orchard Management Software, where you can easily manage your orchard, record harvests, "
          "and create a fruitful orchard experience!")
    global fruit_file
    fruit_info_relative_path = "production/fruits.csv"
    fruit_file = file_import(fruit_info_relative_path)

    global plantation_file
    plantation_relative_path = "production/plantations.csv"
    plantation_file = file_import(plantation_relative_path)

    global extra_productivity_file
    extra_productivity_relative_path = "management/extra_productivity.csv"
    extra_productivity_file = file_import(extra_productivity_relative_path)

    global remaining_productivity_file
    remaining_productivity_path = "management/remaining_productivity.csv"
    remaining_productivity_file = file_import(remaining_productivity_path)

    global inventory_file
    inventory_file_path = "management/inventory.csv"
    inventory_file = file_import(inventory_file_path)

    global order_file
    order_file_path = "management/orders.csv"
    order_file = file_import(order_file_path)

    fruit_init(fruit_file)
    plantation_init(fruit_file, plantation_file)
    inventory_init(extra_productivity_file, remaining_productivity_file, inventory_file)
    sales_init(extra_productivity_file, remaining_productivity_file, inventory_file, order_file)
    basic_choice_select(fruit_file, plantation_file, extra_productivity_file, remaining_productivity_file,
                        inventory_file, order_file)
