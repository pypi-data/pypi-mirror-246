
import os
import sys
# Add the project's root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from test.test_sales import Test_SalesManager
from test.test_discounts import Test_DiscountManager
from test.test_products import TestProductManager
from test.test_stock import TestStockManager, TestPerishableStockManager


def create_suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(Test_DiscountManager))
    suite.addTests(unittest.makeSuite(Test_SalesManager))
    suite.addTests(unittest.makeSuite(TestProductManager))
    suite.addTests(unittest.makeSuite(TestStockManager))
    suite.addTests(unittest.makeSuite(TestPerishableStockManager))
    runner = unittest.TextTestRunner(verbosity=2)
    print(runner.run(suite))

create_suite()
