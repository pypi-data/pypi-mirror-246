import os
import os.path
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import pandas as pd
from unittest.mock import patch
from io import StringIO
from src.orchardmanagementpackage.management.inventory import InventoryManagement
from src.orchardmanagementpackage.management.sales import SalesManagement


class TestSalesManagement(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Setting up class...")
        # Initialize common data for the entire test class
        cls.inventory_origin_df = pd.read_csv("management_testing_files/inventory_origin.csv")
        cls.remaining_productivity_origin_df = pd.read_csv(
            "management_testing_files/remaining_productivity_origin.csv")
        cls.extra_productivity_origin_df = pd.read_csv("management_testing_files/extra_productivity_origin.csv")
        cls.orders_origin_df = pd.read_csv("management_testing_files/orders_origin.csv")

    @classmethod
    def tearDownClass(cls):
        print("Tearing down class...")
        # Clean up any resources for entire class
        cls.inventory_origin_df = None
        cls.remaining_productivity_origin_df = None
        cls.extra_productivity_origin_df = None
        cls.orders_origin_df = None

    def setUp(self):
        print("Setting up test...")
        # Create a temporary DataFrame for testing purposes
        self.inventory_origin_df.to_csv("inventory.csv", index=False)
        self.remaining_productivity_origin_df.to_csv("remaining_productivity.csv", index=False)
        self.extra_productivity_origin_df.to_csv("extra_productivity.csv", index=False)
        self.orders_origin_df.to_csv("orders.csv", index=False)
        self.inventory_manager = InventoryManagement("extra_productivity.csv",
                                                     "remaining_productivity.csv", "inventory.csv")
        self.sales_manager = SalesManagement(self.inventory_manager, "orders.csv")

    def tearDown(self):
        print("Tearing down test...")
        # Clean up any resources used during the test
        del self.inventory_manager
        files_to_remove = ["inventory.csv", "orders.csv", "remaining_productivity.csv", "extra_productivity.csv"]
        for file_name in files_to_remove:
            if os.path.exists(file_name):
                os.remove(file_name)

    @patch('sys.stdout', new_callable=StringIO)
    def test_add_order(self, mock_stdout):
        # wrong sales_type
        self.assertEqual(self.sales_manager.add_order('sale', 'Ambrosia', 10),False, "add_order abnormal")

        # Fruit type 1
        self.sales_manager.add_order('selling', 'Ambrosia', 50)
        self.assertListEqual(list(self.sales_manager.orders.iloc[3]),
                             [4, "selling", 1, "Ambrosia", 50, 1.2, 60.0], "add_order abnormal")
        # Fruit type 2
        self.sales_manager.add_order('picking', 'Lapins', 10)
        self.assertListEqual(list(self.sales_manager.orders.iloc[4]),
                             [5, "picking", 2, "Lapins", 10, 2.99, 29.9], "add_order abnormal")
        # Fruit type 3
        self.sales_manager.add_order('selling', 'Elberta', 20)
        self.assertListEqual(list(self.sales_manager.orders.iloc[5]),
                             [6, 'selling', 3, 'Elberta', 20, 1.2, 24.0], "add_order abnormal")
        # wrong variety
        self.sales_manager.add_order('selling', 'Amb', 10)
        printed_output = mock_stdout.getvalue().strip()
        self.assertIn("Fruit 'Amb' not found.", printed_output, "add_order abnormal")

        # Variety with no instance
        with self.assertRaises(ValueError) as context:
            self.sales_manager.add_order("selling", "Cresthaven", 10)
        self.assertEqual(str(context.exception), "There is no instance of this fruit",
                         "add_order abnormal")

        # Empty orders table
        self.sales_manager.orders = pd.read_csv("orders.csv", nrows=0)
        self.sales_manager.orders.to_csv("orders.csv", index=False)
        self.sales_manager.add_order('selling', 'Ambrosia', 10)
        self.assertListEqual(list(self.sales_manager.orders.iloc[0]),
                             [1, "selling", 1, "Ambrosia", 10, 1.2, 12], "add_order abnormal")

    def test_order_display(self):
        self.assertEqual(self.sales_manager.order_display(), 3, "order_display abnormal")

    @patch('sys.stdout', new_callable=StringIO)
    def test_revenue_display(self, mock_stdout):
        # variable not found
        self.sales_manager.revenue_display("random")
        printed_output = mock_stdout.getvalue().strip()
        self.assertIn("Variable random not found. Please choose from: sales_type or fruit_type.", printed_output,
                      "revenue_display abnormal when variable not found")
        # display by sales_type
        result = self.sales_manager.revenue_display("sales_type")
        expected_result = pd.DataFrame({
            'sales_type': ['picking', 'selling'],
            'revenue': [119.6, 120.0]
        })
        self.assertTrue(result.equals(expected_result), "Actual result does not match expected result")
        # display by fruit_type
        result2 = self.sales_manager.revenue_display('fruit_type')
        expected_result2 = pd.DataFrame({
            'fruit_type': [1, 2, 3],
            'revenue': [60.0, 119.6, 60.0]
        })
        self.assertTrue(result2.equals(expected_result2), "Actual result does not match expected result")
        # Empty orders table
        self.sales_manager.orders = pd.read_csv("orders.csv", nrows=0)
        self.sales_manager.orders.to_csv("orders.csv", index=False)
        self.sales_manager.revenue_display('fruit_type')
        printed_output = mock_stdout.getvalue().strip()
        self.assertIn("No data available.",
                      printed_output, "revenue_display abnormal when orders empty")

    @patch('sys.stdout', new_callable=StringIO)
    def test_check_inventory(self, mock_stdout):
        self.sales_manager.check_inventory("Ambrosia", 10)
        printed_output = mock_stdout.getvalue().strip()
        self.assertIn("Inventory of Ambrosia is enough for this order.",
                      printed_output, "check_inventory abnormal")
        self.sales_manager.check_inventory("Ambrosia", 1000)
        printed_output = mock_stdout.getvalue().strip()
        self.assertIn("Remaining productivity of Ambrosia is 300 kg, which is not enough",
                      printed_output, "check_inventory abnormal")
        self.sales_manager.check_inventory("Amb", 1000)
        printed_output = mock_stdout.getvalue().strip()
        self.assertIn("Error: Amb is not a valid fruit type.",
                      printed_output, "check_inventory abnormal")



if __name__ == '__main__':
    unittest.main()
