import os
import sys
# Add the project's root directory to the Python path
folder_name = "src"
current_dire = os.getcwd()
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
folder_name = os.path.join(current_dire,folder_name)
sys.path.append(folder_name)

import unittest
from groceryManagement.sales_management.discounts import DiscountManager

class Test_DiscountManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_data = [
            ("P0001", 0.10),
            ("P0002", 0.20),
            ("P0003", 0.05),
        ]

    @classmethod
    def tearDownClass(cls):
        del cls.test_data

    def setUp(self):
        self.discount_manager = DiscountManager()
        for product_id, discount in self.test_data:
            self.discount_manager.add_discount(product_id, discount)

    def tearDown(self):
        self.discount_manager = None

    def test_add_discount(self):
        self.discount_manager.add_discount("P0004", 0.15)
        self.assertIn("P0004",self.discount_manager.discounts)
        self.assertEqual(self.discount_manager.discounts["P0004"],0.15)
        self.assertEqual(self.discount_manager.discounts["P0004"], 0.15)
        self.assertGreaterEqual(self.discount_manager.discounts["P0004"], 0)
        self.assertLessEqual(self.discount_manager.discounts["P0004"], 1)

    def test_apply_discount_existing(self):
        price = 100
        product_id = "P0002"
        expected_price = price * (1-self.discount_manager.discounts[product_id])
        discounted_price = self.discount_manager.apply_discount(product_id, price)
        self.assertEqual(discounted_price, expected_price)
        self.assertNotEqual(discounted_price, price)
        self.assertIsInstance(discounted_price, (int, float))
        self.assertLess(discounted_price, price)

    def test_apply_discount_non_existing(self):
        price = 100
        product_id = "P9999"
        discounted_price = self.discount_manager.apply_discount(product_id,price)
        self.assertEqual(discounted_price, price)
        self.assertGreaterEqual(discounted_price, 0)
        self.assertIsInstance(discounted_price, (int, float))
        self.assertFalse(product_id in self.discount_manager.discounts)

if __name__ =='main':
    unittest.main()