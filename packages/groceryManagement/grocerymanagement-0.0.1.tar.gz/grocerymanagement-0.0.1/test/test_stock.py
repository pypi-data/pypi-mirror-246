import os
import sys
# Add the project's root directory to the Python path
folder_name = "src"
current_dire = os.getcwd()
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
folder_name = os.path.join(current_dire,folder_name)
sys.path.append(folder_name)

import unittest
from groceryManagement.inventory_management.stock import StockManager, PerishableStockManager

class TestStockManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Setting up TestStockManager class...")

    @classmethod
    def tearDownClass(cls):
        print("Tearing down TestStockManager class...")

    def setUp(self):
        self.sm = StockManager()

    def tearDown(self):
        del self.sm

    def test_add_remove_stock(self):
        self.sm.add_stock(1, 50)
        self.assertEqual(self.sm.stock[1], 50)
        self.sm.remove_stock(1, 20)
        self.assertEqual(self.sm.stock[1], 30)
        with self.assertRaises(ValueError):
            self.sm.remove_stock(1, 40)

class TestPerishableStockManager(unittest.TestCase):

    def setUp(self):
        self.psm = PerishableStockManager()

    def tearDown(self):
        del self.psm

    def test_add_perishable_stock(self):
        self.psm.add_perishable_stock(1, 50, "2023-12-31")
        self.assertIn(1, self.psm.stock)
        self.assertIn(1, self.psm.perishable_stock)
        self.assertEqual(self.psm.stock[1], 50)
        self.assertEqual(self.psm.perishable_stock[1][0]["expiry_date"], "2023-12-31")

    def test_check_remove_expired_stock(self):
        self.psm.add_perishable_stock(2, 30, "2022-12-31")
        expired = self.psm.check_expiry("2023-01-01")
        self.assertEqual(expired[2], 30)
        self.psm.remove_expired_stock("2023-01-01")
        self.assertNotIn(2, self.psm.perishable_stock)

if __name__ =='main':
    unittest.main()