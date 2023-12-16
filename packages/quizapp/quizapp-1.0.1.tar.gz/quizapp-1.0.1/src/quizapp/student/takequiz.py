from . import readquiz as rq
import random

class Student:
    """ This class bundles student name and student number into individual quiz objects """
    def __init__(self, student_name, student_number) -> None:
        self.student_name = student_name
        self.student_number = student_number
        
def student_handler():
    """ Returns a student object with user inputs of student name and student number """
    student_name = input("Please enter your name:")
    student_number = input("Please enter your student number:")
    return Student(student_name, student_number)

def start_quiz(quiz):
    """
    Student start quiz
    
    It is the driver function that enables a student to enter a quiz, answer questions, and obtain a quiz score.
    
    Parameters
    ----------
    object : quiz
        course code
    
    Returns
    -------
    float : score
    """
    score = 0
    problems = quiz.problems
    for i in range(len(problems)):
        no_of_questions = len(problems)
        ch = random.randint(0, no_of_questions-1)
        print(f'\nQ{i+1}. {problems[ch].question}\n')
        for option in problems[ch].options:
            print(option)
        answer = input("\nEnter your answer: ")
        if problems[ch].answer[0] == answer[0].upper():
            print("\nYou are correct")
            score+=1
        else:
            print("\nYou are incorrect")
        del problems[ch]
    score = round(score / quiz.no_of_problems * 100, 2)
    return score

def select_quiz():
    """
    Select a quiz 
    
    It displays all available quizzes then prompts a student to select a quiz to complete. Then it calculates and
    displays overall quiz average via get_percentage() in the readquiz module if the student prompts the function.
    """
    student = student_handler()
    print("Welcome", student.student_name)
    print("Quizzes for these courses are available:")
    courses = rq.get_available_courses()
    course_dict = {}
    for i in range(len(courses)):
        print(i+1, '.', courses[i])
        course_dict[i+1] = courses[i]
    course_input = int(input("Enter your choice:"))
    if course_input not in list(course_dict.keys()):
        print("No such quiz available.")
        return
    course_code = course_dict.get(course_input)
    quiz = rq.read_quiz(course_code)
    score = start_quiz(quiz)
    success = rq.save_score(student, course_code, score)
    if success:
        print("Your score is:", score, "and it was saved successfully.")
    print("Do you want to calculate overall percentage?")
    print("1. Yes \n2. No")
    calc_percentage_flag = int(input("Enter response:"))
    if calc_percentage_flag == 1:
        percentage = rq.get_percentage(student)
        print("Your overall percentage across all courses is:", percentage)