import pandas as pd
import matplotlib.pyplot as plt


class SalesManagement:
    """
    A class for managing sales operations, including order processing, revenue analysis, and inventory checks.

    Attributes:
    - inventory_manager (InventoryManagement): An instance of the InventoryManagement class.
    - fruit_file (str): The path to the file containing fruit information.
    - order_file (str): The path to the file containing sales orders.
    - orders (pd.DataFrame): DataFrame to store sales order data.
    """

    def __init__(self, inventory_manager, order_file):
        """
        Initialize a SalesManagement instance.
        """
        self.inventory_manager = inventory_manager
        self.order_file = order_file
        self.orders = self.load_data()

    def load_data(self):
        """
        Load sales order data from a CSV file.

        Returns:
        - pd.DataFrame: DataFrame containing sales order data.
        """
        columns = ["index", "sales_type", "fruit_type", "fruit_variety", "weight", "unit_price", "revenue"]
        try:
            orders_data = pd.read_csv(self.order_file)
        except FileNotFoundError:
            # If the file doesn't exist, return an initial empty DataFrame
            orders_data = pd.DataFrame(columns=columns)
            orders_data.to_csv(self.order_file, index=True)
        return orders_data

    def add_order(self, sales_type, fruit_variety, weight):
        """
        Add a new sales order.

        Parameters:
        - sales_type (str): The type of sales operation ('selling' or 'picking').
        - fruit_variety (str): The variety of fruit for the order.
        - weight (float): The weight of the fruit in the order.
        """
        if fruit_variety not in self.inventory_manager.inventory.columns:
            print(f"Fruit '{fruit_variety}' not found.")
            return
        else:
            # file setting
            if sales_type == "selling":
                if not self.inventory_manager.remove_inventory(fruit_variety, weight):
                    print("Order cannot be added.")
                else:
                    self.inventory_manager.remove_inventory(fruit_variety, weight)
                    print("Order added")
            elif sales_type == "picking":
                self.inventory_manager.remove_remaining_productivity(fruit_variety, weight)
                print("Order added")
            else:
                print("sales_type not found, please choose from selling and picking")
                return False
            # index setting
            if self.orders.empty:
                new_index = 1
            else:
                new_index = self.orders["index"].max() + 1
            # fruit variety setting
            if fruit_variety in ["Ambrosia", "Gala", "Honeycrisp"]:
                fruit_type_num = 1
            elif fruit_variety in ["Lapins", "Sweetheart", "Skeena"]:
                fruit_type_num = 2
            elif fruit_variety in ["Redhaven", "Elberta", "Cresthaven"]:
                fruit_type_num = 3
            else:
                print("Variety not found")
                return False

            if fruit_variety == "Ambrosia":
                unit_price = 1.20
            elif fruit_variety == "Elberta":
                unit_price = 1.20
            elif fruit_variety == "Lapins":
                unit_price = 2.99
            else:
                raise ValueError("There is no instance of this fruit")

            new_order = pd.DataFrame(columns=self.orders.columns)
            new_order = pd.DataFrame({
                "index": [new_index],
                "sales_type": [sales_type],
                "fruit_type": [fruit_type_num],
                "fruit_variety": [fruit_variety],
                "weight": [weight],
                "unit_price": [unit_price],
                "revenue": [round(weight * unit_price, 2)]
            })

            self.orders = pd.concat([self.orders, new_order], ignore_index=True)
            self.orders.to_csv(self.order_file, index=False)
            return True

    def order_display(self):
        """
        Display the sales order data.
        """
        print(self.orders)
        return len(self.orders)

    def revenue_display(self, variable):
        """
        Display revenue data based on a specified variable.

        Parameters:
        - variable (str): The variable for grouping revenue data.
        """
        if variable not in self.orders.columns:
            print(f"Variable {variable} not found. Please choose from: sales_type or fruit_type.")
            return

        if not self.orders.empty:
            # Display the entire DataFrame
            revenue_by_variable = self.orders.groupby(variable)['revenue'].sum().reset_index()
            print(revenue_by_variable)
            return pd.DataFrame(revenue_by_variable)
        else:
            print("No data available.")

    def revenue_plotter(self):
        """
        Plot a pie chart of revenue distribution by fruit type.
        """
        if self.orders.empty:
            print("No data available for plotting.")
            return

        fruit_type_mapping = {
            1: 'Apple',
            2: 'Cherry',
            3: 'Peach'
        }

        self.orders['fruit_type_label'] = self.orders['fruit_type'].map(fruit_type_mapping)
        revenue_by_fruit_type = self.orders.groupby('fruit_type_label')['revenue'].sum().reset_index()

        plt.figure(figsize=(8, 8))
        plt.pie(revenue_by_fruit_type['revenue'], labels=revenue_by_fruit_type['fruit_type_label'],
                autopct='%1.1f%%', startangle=140)
        plt.title('Revenue Distribution by Fruit Type')
        plt.show()

    def check_inventory(self, fruit_variety, weight):
        """
        Checks if selling a specified quantity of fruits is possible.

        Parameters:
        - fruit_variety (str): The variety of fruit for the inventory check.
        - weight (float): The weight of the fruit to be sold.
        """
        current_inventory = self.inventory_manager.inventory.iloc[[-1]].copy()

        if fruit_variety in current_inventory.columns:
            inventory_weight = current_inventory[fruit_variety].iloc[0]
            print(inventory_weight)
            if inventory_weight >= weight:
                print(f"Inventory of {fruit_variety} is enough for this order.")
            else:
                print(f"Remaining productivity of {fruit_variety} is {inventory_weight} kg, which is not enough")
        else:
            print(f"Error: {fruit_variety} is not a valid fruit type.")
