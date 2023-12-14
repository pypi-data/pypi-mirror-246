import os
import os.path
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from unittest.mock import patch
from io import StringIO
from src.orchardmanagement_package.management.inventory import InventoryManagement, HistoricalPlotter


class TestInventoryManagement(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Setting up class...")
        # Initialize common data for the entire test class
        cls.inventory_origin_df = pd.read_csv("management_testing_files/inventory_origin.csv")
        cls.remaining_productivity_origin_df = pd.read_csv(
            "management_testing_files/remaining_productivity_origin.csv")
        cls.extra_productivity_origin_df = pd.read_csv(
            "management_testing_files/extra_productivity_origin.csv")

    @classmethod
    def tearDownClass(cls):
        print("Tearing down class...")
        # Clean up any resources for entire class
        cls.inventory_origin_df = None
        cls.remaining_productivity_origin_df = None
        cls.extra_productivity_origin_df = None

    def setUp(self):
        print("Setting up test...")
        # Create a temporary DataFrame for testing purposes
        self.inventory_origin_df.to_csv("inventory.csv", index=False)
        self.remaining_productivity_origin_df.to_csv("remaining_productivity.csv", index=False)
        self.extra_productivity_origin_df.to_csv("extra_productivity.csv", index=False)
        self.inventory_manager = InventoryManagement("extra_productivity.csv",
                                                     "remaining_productivity.csv", "inventory.csv")

    def tearDown(self):
        print("Tearing down test...")
        # Clean up any resources used during the test
        del self.inventory_manager
        files_to_remove = ["inventory.csv", "orders.csv", "remaining_productivity.csv", "extra_productivity.csv"]
        for file_name in files_to_remove:
            if os.path.exists(file_name):
                os.remove(file_name)


    def test_total_product_estimate(self):
        self.inventory_manager.remaining_productivity = pd.read_csv("remaining_productivity.csv", nrows=0)
        self.inventory_manager.remaining_productivity.to_csv("remaining_productivity.csv", index=False)
        self.inventory_manager.total_product_estimate()
        # normal condition
        self.assertListEqual(list(self.inventory_manager.remaining_productivity.iloc[0]),
                             [1, 30000, 0, 0, 40000, 0, 0, 0, 72000, 0], "First rows are not equal")
        with self.assertRaises(ValueError) as context:
            self.inventory_manager.total_product_estimate()
        # As this is the initiation of remaining_productivity raise error when file is not empty
        self.assertEqual(str(context.exception), "File is not empty, and cannot be initialized by total capacity")

    def test_add_inventory(self):
        self.inventory_manager.add_inventory("Ambrosia", 10)
        self.assertListEqual(list(self.inventory_manager.inventory.iloc[2]),
                             [3, 310, 0, 0, 0, 0, 0, 0, 400, 0], "add_inventory abnormal")
        with self.assertRaises(ValueError) as context:
            self.inventory_manager.add_inventory("Ambro", 10)
        # Fruit not found
        self.assertEqual(str(context.exception), "Fruit not found in inventory")

    def test_add_extra_productivity(self):
        self.inventory_manager.add_inventory("Gala", 100)  # Gala's remaining capacity is 0 and will add on extra file
        self.assertListEqual(list(self.inventory_manager.extra_productivity.iloc[1]),
                             [2, 0, 200, 50, 0, 0, 0, 0, 0, 0], "add_extra_productivity abnormal")

    @patch('sys.stdout', new_callable=StringIO)
    def test_remove_inventory(self, mock_stdout):
        # normal condition
        self.inventory_manager.remove_inventory("Ambrosia", 100)
        self.assertListEqual(list(self.inventory_manager.inventory.iloc[2]),
                             [3, 200, 0, 0, 0, 0, 0, 0, 400, 0], "remove_inventory abnormal")
        self.inventory_manager.remove_inventory("Elberta", 100)
        self.assertListEqual(list(self.inventory_manager.inventory.iloc[3]),
                             [4, 200, 0, 0, 0, 0, 0, 0, 300, 0], "remove_inventory abnormal")

        # fruit not exists
        with self.assertRaises(ValueError) as context:
            self.inventory_manager.add_inventory("Ambro", 10)
        self.assertEqual(str(context.exception), "Fruit not found in inventory",
                         "remove_inventory abnormal when fruit not found")

        # inventory not enough
        self.inventory_manager.remove_inventory("Ambrosia", 500)
        printed_output = mock_stdout.getvalue().strip()
        self.assertIn("Not enough Ambrosia in inventory, only 200 left", printed_output,
                      "remove_inventory abnormal when lack of inventory")

        # inventory empty
        self.inventory_manager.inventory = pd.read_csv("inventory.csv", nrows=0)
        self.inventory_manager.inventory.to_csv("inventory.csv", index=False)

        self.inventory_manager.remove_inventory("Elberta", 100)
        printed_output2 = mock_stdout.getvalue().strip()
        self.assertIn("Inventory is empty.", printed_output2, "remove_inventory abnormal when inventory is empty")

    @patch('sys.stdout', new_callable=StringIO)
    def test_remove_remaining_productivity(self, mock_stdout):
        # normal condition
        self.inventory_manager.remove_remaining_productivity("Ambrosia", 500)
        self.assertListEqual(list(self.inventory_manager.remaining_productivity.iloc[-1]),
                             [2, 29500, 0, 0, 40000, 0, 0, 0, 72000, 0], "remove_remaining_productivity abnormal")

        # Fruit not exists
        self.inventory_manager.remove_remaining_productivity("Elb", 100)
        printed_output = mock_stdout.getvalue().strip()
        self.assertIn("Fruit 'Elb' not found", printed_output,
                      "remove_remaining_productivity abnormal when fruit not found")

        # the inventory added exceed the remaining capacity
        self.inventory_manager.add_inventory("Gala", 100)
        printed_output2 = mock_stdout.getvalue().strip()
        self.assertIn("The product of Gala exceeds expectations and will be recorded in the extra_productivity file.",
                      printed_output2,
                      "remove_remaining_productivity abnormal when inventory exceed estimate")

        # Production decrease record exceeds the remaining capacity
        self.inventory_manager.remove_remaining_productivity("Gala", 100, 1)
        printed_output3 = mock_stdout.getvalue().strip()
        self.assertIn("The estimated yield will be set to 0", printed_output3,
                      "remove_remaining_productivity abnormal when production decrease")

        # remaining productivity not initialized
        self.inventory_manager.remaining_productivity = pd.read_csv("remaining_productivity.csv", nrows=0)
        self.inventory_manager.remaining_productivity.to_csv("remaining_productivity.csv", index=False)
        self.inventory_manager.remove_remaining_productivity("Ambrosia", 500)
        printed_output4 = mock_stdout.getvalue().strip()
        self.assertIn("Please estimate capacity first.", printed_output4,
                      "remove_remaining_productivity abnormal when data not initialized")

    @patch('sys.stdout', new_callable=StringIO)
    def test_get_current_inventory(self, mock_stdout):
        # normal condition
        self.assertListEqual(self.inventory_manager.get_current_inventory(), [2, 300, 0, 0, 0, 0, 0, 0, 400, 0],
                             "get_current_inventory abnormal")

        # empty inventory
        self.inventory_manager.inventory = pd.read_csv("inventory.csv", nrows=0)
        self.inventory_manager.inventory.to_csv("inventory.csv", index=False)
        self.inventory_manager.get_current_inventory()
        printed_output = mock_stdout.getvalue().strip()
        self.assertIn("Inventory is empty.", printed_output, "get_current_inventory abnormal when empty")

    def test_get_remaining_productivity(self):
        self.assertListEqual(self.inventory_manager.get_remaining_productivity(),
                             [1, 30000, 0, 0, 40000, 0, 0, 0, 72000, 0], "get_remaining_productivity abnormal")

    def test_get_extra_productivity(self):
        self.assertListEqual(self.inventory_manager.get_extra_productivity(), [1, 0, 100, 50, 0, 0, 0, 0, 0, 0],
                             "get_extra_productivity abnormal")


class TestHistoricalPlotter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Setting up class...")
        # Initialize common data for the entire test class
        cls.inventory_origin_df = pd.read_csv("management_testing_files/inventory_origin.csv")
        cls.remaining_productivity_origin_df = pd.read_csv(
            "management_testing_files/remaining_productivity_origin.csv")

    @classmethod
    def tearDownClass(cls):
        print("Tearing down class...")
        # Clean up any resources for entire class
        cls.inventory_origin_df = None
        cls.remaining_productivity_origin_df = None

    def setUp(self):
        print("Setting up test...")
        # Create a temporary DataFrame for testing purposes
        self.inventory_origin_df.to_csv("inventory.csv", index=False)
        self.remaining_productivity_origin_df.to_csv("remaining_productivity.csv", index=False)
        self.plotter = HistoricalPlotter("remaining_productivity.csv", "inventory.csv")

    def tearDown(self):
        print("Tearing down test...")
        # Clean up any resources used during the test
        del self.plotter
        files_to_remove = ["inventory.csv", "remaining_productivity.csv"]
        for file_name in files_to_remove:
            if os.path.exists(file_name):
                os.remove(file_name)

    def test_plot_historical_data(self):
        result = self.plotter.plot_historical_data(3, 1)
        self.assertEqual("Inventory Management - Peach", result, "plot_historical_data abnormal")
        with patch('pandas.read_csv') as mock_read_csv, patch('matplotlib.pyplot.show'):
            self.plotter.plot_historical_data(1, 1)
        mock_read_csv.assert_called_once_with("inventory.csv")
        with patch('pandas.read_csv') as mock_read_csv, patch('matplotlib.pyplot.show'):
            self.plotter.plot_historical_data(2, 2)
        mock_read_csv.assert_called_once_with("remaining_productivity.csv")


if __name__ == '__main__':
    unittest.main()
