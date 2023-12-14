import os
import sys
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest_modules.fruit_unittest import FruitTestCase
from unittest_modules.fruit_unittest import FruitInfoTestCase
from unittest_modules.fruit_unittest import FruitInfoAddRemoveTestCase
from unittest_modules.plantation_unittest import RegionTestCase
from unittest_modules.unittest_inventory import TestInventoryManagement
from unittest_modules.unittest_inventory import TestHistoricalPlotter
from unittest_modules.unittest_sales import TestSalesManagement


def my_suite():
    suite = unittest.TestSuite()
    result = unittest.TestResult()

    suite.addTest(unittest.makeSuite(FruitTestCase))
    suite.addTest(unittest.makeSuite(FruitInfoTestCase))
    suite.addTest(unittest.makeSuite(FruitInfoAddRemoveTestCase))
    suite.addTest(unittest.makeSuite(RegionTestCase))
    suite.addTest(unittest.makeSuite(TestInventoryManagement))
    suite.addTest(unittest.makeSuite(TestHistoricalPlotter))
    suite.addTest(unittest.makeSuite(TestSalesManagement))

    runner = unittest.TextTestRunner()
    print(runner.run(suite))
if __name__ == '__main__':
    my_suite()

