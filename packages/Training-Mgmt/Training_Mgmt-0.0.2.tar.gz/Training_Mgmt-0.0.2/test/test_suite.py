import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_Exercise_Exercise import TestExercise
from test_Exercise_Record import TestRecord
from calculate_test import TestCalculate
from person_test import TestPerson
from record_test import TestRecord as RT

def my_suite():
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    suite.addTest(TestExercise('test_set_intensity'))
    suite.addTest(TestExercise('test_set_bodypart'))
    suite.addTest(TestExercise('test_cardio_suggestion'))
    suite.addTest(TestExercise('test_strength_suggestion'))
    suite.addTest(TestExercise('test_hybrid_suggestion'))
    suite.addTest(TestExercise('test_strength_choices_helper'))
    
    suite.addTest(TestRecord('test_add'))
    suite.addTest(TestRecord('test_remove_by_index'))
    suite.addTest(TestRecord('test_modify'))

    suite.addTest(TestCalculate('test_bmr_type'))
    suite.addTest(TestCalculate('test_bmr'))
    suite.addTest(TestCalculate('test_tdee'))
    suite.addTest(TestCalculate('test_calorie'))
    suite.addTest(TestCalculate('test_nutrition_bulking'))


    suite.addTest(TestPerson('test_name'))
    suite.addTest(TestPerson('test_age'))
    suite.addTest(TestPerson('test_height'))
    suite.addTest(TestPerson('test_weight'))
    suite.addTest(TestPerson('test_gender'))
    suite.addTest(TestPerson('test_purpose'))
    suite.addTest(TestPerson('test_frequency'))

    suite.addTest(TestPerson('test_name'))
    suite.addTest(TestPerson('test_age'))
    suite.addTest(TestPerson('test_height'))
    suite.addTest(TestPerson('test_weight'))
    suite.addTest(TestPerson('test_gender'))
    suite.addTest(TestPerson('test_purpose'))
    suite.addTest(TestPerson('test_frequency'))

    suite.addTest(RT('test_add_new_record'))
    suite.addTest(RT('test_add_existing_record'))
    suite.addTest(RT('test_remove_record'))
    suite.addTest(RT('test_remove_not_existing_record'))
    suite.addTest(RT('test_remove_not_existing_record_2'))
    suite.addTest(RT('test_modify_record'))
    suite.addTest(RT('test_modify_not_existing_record'))
    suite.addTest(RT('test_show'))

    runner = unittest.TextTestRunner()
    print(runner.run(suite))

my_suite()

