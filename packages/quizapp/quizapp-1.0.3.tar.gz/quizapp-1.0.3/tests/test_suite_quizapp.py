import unittest

from readquiz_test import ReadQuizTest
from takequiz_test import TakeQuizTest
from createquiz_test import CreateQuizTest
# from checkstudentscore_test import CheckStudentScoreTest
# from main_test import MainTest

def quizapp_test_suite():
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    suite.addTest(ReadQuizTest('test_read_quiz'))
    suite.addTest(ReadQuizTest('test_get_available_courses'))
    suite.addTest(ReadQuizTest('test_save_score'))
    suite.addTest(ReadQuizTest('test_get_percentage'))
    suite.addTest(TakeQuizTest('test_student_handler'))
    suite.addTest(TakeQuizTest('test_select_quiz'))
    suite.addTest(CreateQuizTest("test_create_quiz"))
    suite.addTest(CreateQuizTest("test_convert_to_json"))
    suite.addTest(CreateQuizTest("test_create_score_csv"))
    suite.addTest(CreateQuizTest("test_create_quiz"))
    # Tests work, issue with python version in Travis for these:  
    
    # suite.addTest(CheckStudentScoreTest("test_score_driver"))
    # suite.addTest(CheckStudentScoreTest("test_quiz_or_score"))
    # suite.addTest(MainTest("test_start"))
    # suite.addTest(MainTest("test_start_2"))
    # suite.addTest(MainTest("test_start_3"))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))
quizapp_test_suite()