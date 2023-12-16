import json
import random
import os
import csv

from os.path import isfile, join

# Constants
QUIZ_FILE_DIRECTORY = "../assets/quizzes/"
SCORE_FILE_DIRECTORY = "../assets/scores/"
UNDERSCORE = '_'
SCORES = 'scores'

# Set current directory to read from absolute path
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

class Quiz:
    """ This class bundles question, problem, and total number of problems into individual quiz objects"""
    def __init__(self, name, problems):
        self.name = name
        self.problems = problems
        self.no_of_problems = len(problems)
        
class Problem:
    """ This class bundles individual questions, multiple choice options, and answers into individual problem objects"""
    def __init__(self, ques, options, ans):
        self.question = ques
        self.options = options
        self.answer = ans

# Read quiz from json
def read_quiz(course_code):
    """
    Read a quiz
    
    It outputs a quiz to the screen by taking course code as an argument.
    
    Parameters
    ----------
    string : course_code
        course code
    """

    file_name = QUIZ_FILE_DIRECTORY + course_code + ".json"
    problems = []
    with open(file_name, 'r+') as f:
        j = json.load(f)
        for i in range(len(j)):
            no_of_questions = len(j)
            ch = random.randint(0, no_of_questions-1)
            problem = Problem(j[ch]["question"], j[ch]["options"], j[ch]["answer"][0])
            problems.append(problem)
            del j[ch]
    quiz = Quiz(course_code, problems)
    return quiz

def get_available_courses():
    """
    Get a list of available courses
    
    It displays the all courses a student has access to in order to start.
    
    Returns
    ----------
    list : course_names
        a list of all courses
    """
    filedir = QUIZ_FILE_DIRECTORY
    files = [f for f in os.listdir(filedir) if f.endswith('.json')]
    course_names = [f.split('.', 1)[0] for f in files]
    return course_names

def save_score(student, course_code, score):
    """
    Save quiz score
    
    It saves the quiz score for a student into a csv file by taking student, course code, and score as arguments.
    
    Parameters
    ----------
    object : student
        course code
    string : course_code
        course code
    int : score
        quiz score

    Returns
    ----------
    boolean : True
    """
    score_row = [student.student_number, student.student_name, score]
    filename = SCORE_FILE_DIRECTORY + course_code + UNDERSCORE + SCORES + ".csv"
    with open(filename, 'a') as csvfile:
        scorewriter = csv.writer(csvfile)
        scorewriter.writerow(score_row)
        csvfile.close()
    return True

def get_percentage(student):
    """
    Get quiz score percentage
    
    It displays the student's quiz score averaged across quizzes as a percentage by taking student as an argument.
    
    Parameters
    ----------
    object : student
        student name
    
    Returns
    --------
    float : average_percentage
        average score across quizzes
    """
    courses = get_available_courses()
    total_scored = 0.0
    number_of_courses = 0
    average_percentage = 0.0
    for course in courses:
        filename = SCORE_FILE_DIRECTORY + course + UNDERSCORE + SCORES + ".csv"
        with open(filename) as score_file:
            reader = csv.DictReader(score_file)
            for row in reader:
                if row['student_number'] == student.student_number:
                    total_scored += float(row['score'])
                    number_of_courses += 1
    if number_of_courses != 0:
        average_percentage = total_scored / number_of_courses
    return average_percentage
                
        