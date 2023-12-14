import unittest
from planoptions_test import TestPlanOptions
from dietoptions_test import TestDietOptions


def my_suite():
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    suite.addTest(TestPlanOptions('setUpClass'))
    suite.addTest(TestPlanOptions('tearDownClass'))
    suite.addTest(TestPlanOptions('setUp'))
    suite.addTest(TestPlanOptions('tearDown'))
    suite.addTest(TestPlanOptions('test_calculate_bmr'))
    suite.addTest(TestPlanOptions('test_calculate_tdee'))
    suite.addTest(TestPlanOptions('test_calculate_target_cal'))
    suite.addTest(TestDietOptions('setUpClass'))
    suite.addTest(TestDietOptions('tearDownClass'))
    suite.addTest(TestDietOptions('setUp'))
    suite.addTest(TestDietOptions('tearDown'))
    suite.addTest(TestDietOptions('test_generate_vegan_meal'))
    suite.addTest(TestDietOptions('test_generate_vegetarian_meal'))
    suite.addTest(TestDietOptions('test_generate_meat_meal'))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))
    
my_suite()