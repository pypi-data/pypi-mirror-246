import pandas as pd
import matplotlib.pyplot as plt


class HistoricalPlotter:
    """
    A class for plotting historical data related to inventory management and remaining capacity.
    """

    def __init__(self, remaining_productivity_file, inventory_file):
        """
        Initialize a HistoricalPlotter instance.

        Parameters:
        - remaining_productivity_file (str): The file path for the remaining productivity data.
        - inventory_file (str): The file path for the inventory data.
        """
        self.inventory_file = inventory_file
        self.remaining_productivity_file = remaining_productivity_file

    def plot_historical_data(self, fruit_category, file_type):
        """
        Plot historical data based on the specified fruit category and file type.

        Parameters:
        - fruit_category (int): The category of fruit (1-Apple, 2-Cherry, 3-Peach).
        - file_type (int): The type of file to use (1 for inventory, 2 for remaining capacity).
        """
        if file_type == 1:
            data = pd.read_csv(self.inventory_file)
            title_file = "Inventory Management"
        else:
            data = pd.read_csv(self.remaining_productivity_file)
            title_file = "Remaining Capacity"

        x = range(1, len(data) + 1)
        if fruit_category == 1:
            labellist = ["Ambrosia", "Gala", "Honeycrisp"]
            plt.stackplot(x, data.loc[:, 'Ambrosia'], data.loc[:, 'Gala'],
                          data.loc[:, 'Honeycrisp'], labels=labellist)
            title_type = "Apple"
        elif fruit_category == 2:
            labellist = ["Lapins", "Sweetheart", "Skeena"]
            plt.stackplot(x, data.loc[:, "Lapins"], data.loc[:, "Sweetheart"],
                          data.loc[:, "Skeena"], labels=labellist)
            title_type = "Cherry"
        else:
            labellist = ["Redhaven", "Elberta", "Cresthaven"]
            plt.stackplot(x, data.loc[:, "Redhaven"], data.loc[:, "Elberta"],
                          data.loc[:, "Cresthaven"], labels=labellist)
            title_type = "Peach"
        title = f"{title_file} - {title_type}"
        plt.title(title)
        plt.xlabel('Index')
        plt.ylabel('Quantity')
        plt.legend()
        plt.show()
        return title


class InventoryManagement:
    """
    A class for managing inventory, remaining capacity, and extra productivity.

    """

    def __init__(self, extra_productivity_file, remaining_productivity_file, inventory_file):
        """
        Initialize an InventoryManagement instance.

        """
        self.extra_productivity_file = extra_productivity_file
        self.remaining_productivity_file = remaining_productivity_file
        self.inventory_file = inventory_file
        self.inventory, self.remaining_productivity, self.extra_productivity = self.load_data()

    def load_data(self):
        """
        Load data from CSV files (inventory, remaining productivity, extra productivity).

        """
        columns = ["index", "Ambrosia", "Gala", "Honeycrisp", "Lapins", "Sweetheart", "Skeena", "Redhaven", "Elberta",
                   "Cresthaven"]
        try:
            inventory_data = pd.read_csv(self.inventory_file)
        except FileNotFoundError:
            # If the file doesn't exist, return an initial empty inventory
            inventory_data = pd.DataFrame(columns=columns)
            inventory_data.to_csv(self.inventory_file, index=True)

        try:
            remaining_productivity_data = pd.read_csv(self.remaining_productivity_file)
        except FileNotFoundError:
            # If the file doesn't exist, return an initial empty remaining productivity
            remaining_productivity_data = pd.DataFrame(columns=columns)
            remaining_productivity_data.to_csv(self.remaining_productivity_file, index=True)

        try:
            extra_productivity_data = pd.read_csv(self.extra_productivity_file)
        except FileNotFoundError:
            # If the file doesn't exist, return an initial empty extra productivity
            extra_productivity_data = pd.DataFrame(columns=columns)
            extra_productivity_data.to_csv(self.extra_productivity_file, index=True)

        return inventory_data, remaining_productivity_data, extra_productivity_data

    def save_data(self, newdata, filename):
        """
        Save new data to the specified CSV file.

        Parameters:
        - newdata (list): New data to be added to the DataFrame.
        - filename (str): Name of the CSV file to save the data.
        """
        if len(newdata) == 9:
            info = [1]
            info.extend(newdata)
            self.remaining_productivity.loc[len(self.remaining_productivity)] = info
            self.remaining_productivity.to_csv(self.remaining_productivity_file, index=False)
        else:
            try:
                if filename == 1:
                    self.inventory = pd.concat([self.inventory, newdata], ignore_index=True)
                    self.inventory.to_csv(self.inventory_file, index=False)
                elif filename == 2:
                    self.remaining_productivity = pd.concat([self.remaining_productivity, newdata], ignore_index=True)
                    self.remaining_productivity.to_csv(self.remaining_productivity_file, index=False)
                else:
                    self.extra_productivity = pd.concat([self.extra_productivity, newdata], ignore_index=True)
                    self.extra_productivity.to_csv(self.extra_productivity_file, index=False)

            except FileNotFoundError:
                print(f"There is no {filename} file")
            except Exception:
                print("Fail to save data")

    def total_product_estimate(self):
        """
        Estimate total production based on the number of fruit trees and update inventory and remaining productivity.
        """
        if len(self.remaining_productivity) > 0:
            raise ValueError("File is not empty, and cannot be initialized by total capacity")

        plantation_summary = {
            'type_num': [1] * 3 + [2] * 3 + [3] * 3,
            'variety': ["Ambrosia", "Gala", "Honeycrisp", "Lapins", "Sweetheart", "Skeena", "Redhaven", "Elberta",
                        "Cresthaven"],
            'total_area': [20, 0, 0, 40, 0, 0, 0, 40, 0],
        }

        plantation_summary = pd.DataFrame(plantation_summary)
        plantation_summary['avgProduct'] = [1500, 1200, 1800, 1000, 2500, 3500, 2000, 1800, 2200]
        plantation_summary['totalProd'] = plantation_summary['total_area'] * plantation_summary['avgProduct']

        pivot_df = plantation_summary.pivot_table(columns='variety', values='totalProd', fill_value=0)
        pivot_df.reset_index(drop=True, inplace=True)
        desired_order = ["Ambrosia", "Gala", "Honeycrisp", "Lapins", "Sweetheart", "Skeena", "Redhaven", "Elberta",
                         "Cresthaven"]
        pivot_df = pivot_df[desired_order]

        new_row = list(pivot_df.iloc[0, ])
        self.save_data(new_row, self.remaining_productivity_file)

        return True

    def add_inventory(self, fruit_type, number):
        """
        Add inventory of a specific fruit type.

        Parameters:
        - fruit_type (str): The variety of fruit for inventory addition.
        - number (int): The quantity of fruit to add to the inventory.
        """
        if fruit_type not in self.inventory.columns:
            raise ValueError("Fruit not found in inventory")
        else:
            if self.inventory.empty:
                current_inventory = pd.DataFrame([[0] * len(self.inventory.columns)], columns=self.inventory.columns)
            else:
                current_inventory = self.inventory.iloc[[-1]].copy()
            new_row = current_inventory
            new_row[fruit_type] += number
            new_row["index"] = new_row["index"].max() + 1
            self.save_data(new_row, 1)
            self.remove_remaining_productivity(fruit_type, number)

    def add_extra_productivity(self, fruit_type, number):
        """
        Add extra productivity of a specific fruit type.

        Parameters:
        - fruit_type (str): The variety of fruit for extra productivity addition.
        - number (int): The quantity of extra productivity to add.
        """
        if self.extra_productivity.empty:
            current_extra = pd.DataFrame([[0] * len(self.extra_productivity.columns)],
                                         columns=self.extra_productivity.columns)
        else:
            current_extra = self.extra_productivity.iloc[[-1]].copy()
        new_row = current_extra
        new_row[fruit_type] += number
        new_row["index"] = new_row["index"].max() + 1
        self.save_data(new_row, 3)

    def remove_inventory(self, fruit_type, number):
        """
        Remove inventory of a specific fruit type.

        Parameters:
        - fruit_type (str): The variety of fruit for inventory removal.
        - number (int): The quantity of fruit to remove from the inventory.
        """
        if fruit_type not in self.inventory.columns:
            raise ValueError("Fruit not found in inventory")
        else:
            if self.inventory.empty:
                print("Inventory is empty.")
                return False
            else:
                current_inventory = self.inventory.iloc[[-1]].copy()
                current_number = current_inventory.at[current_inventory.index[-1], fruit_type]
                if current_number < number:
                    print(f"Not enough {fruit_type} in inventory, only {current_number} left")
                    return False
                new_row = current_inventory
                new_row[fruit_type] -= number
                new_row["index"] = new_row["index"].max() + 1
                self.save_data(new_row, 1)
        return True

    def remove_remaining_productivity(self, fruit_type, number, direct = 0):
        """
        Remove productivity for a specific fruit type.

        Args:
            fruit_type (str): The type of fruit for which productivity needs to be removed.
            number (int): The quantity of productivity to be removed.
            direct (int): 0 when cased by sales or inventory increase, 1 when cased by other reasons

        Returns:
            None
        """
        if fruit_type not in self.remaining_productivity.columns:
            print(f"Fruit '{fruit_type}' not found.")
            return
        else:
            # check empty
            if self.remaining_productivity.empty:
                print("Please estimate capacity first.")
                return
            else:
                current_capacity = self.remaining_productivity.iloc[[-1]].copy()

                # Check if there's enough quantity to remove
                current_number = current_capacity.at[current_capacity.index[-1], fruit_type]
                new_row = current_capacity
                if current_number < number:
                    if direct == 0 :
                        new_row[fruit_type] = 0
                        print(
                            f"The product of {fruit_type} exceeds expectations and will be recorded in the extra_productivity file.")
                        extra_number = number - current_number
                        self.add_extra_productivity(fruit_type, extra_number)
                    else:
                        print("The estimated yield will be set to 0")
                        new_row[fruit_type] = 0
                else:
                    new_row[fruit_type] -= number
                # set new index number
                new_row["index"] = new_row["index"].max() + 1
                self.save_data(new_row, 2)

    def get_current_inventory(self):
        """
        Get the current inventory status.

        Returns:
            pd.DataFrame: A DataFrame representing the current inventory status.
        """
        if not self.inventory.empty:
            print(self.inventory.iloc[[-1]])
            return list(self.inventory.iloc[-1])
        else:
            print("Inventory is empty.")
            return None

    def get_remaining_productivity(self):
        """
        Get the remaining productivity status.

        Returns:
            pd.DataFrame: A DataFrame representing the current remaining productivity status.
        """
        print(self.remaining_productivity.iloc[[-1]])
        return list(self.remaining_productivity.iloc[-1])

    def get_extra_productivity(self):
        """
        Get the extra productivity status.

        Returns:
            pd.DataFrame: A DataFrame representing the current extra productivity status.
        """
        print(self.extra_productivity.iloc[[-1]])
        return list(self.extra_productivity.iloc[-1])

