import os
import pandas as pd
import numpy as np
import statistics as stats
from teacher import createquiz as cq

# Constants
SCORE_FILE_DIRECTORY = "../assets/scores/"
UNDERSCORE = '_'
SCORES = 'scores'


def get_student_scores(course, stdnum):
    """
    View a students quiz results
    
    It displays the student's quiz score for a course by taking student number
    and course code as arguments.
    
    Parameters
    ----------
    string : course
        course code
    string : stdnum
        student number of the student
    """
    filename = SCORE_FILE_DIRECTORY + course + UNDERSCORE + SCORES + ".csv"
    if os.path.exists(filename):
        scores_table = pd.read_csv(filename, skipinitialspace = True)
        stdnum_list = list(scores_table["student_number"])
        if stdnum in stdnum_list:
            location = np.where(scores_table["student_number"] == stdnum)[0][0]
            name = scores_table.at[location, "student_name"]
            stdnum = str(scores_table.at[location, "student_number"])
            score = str(scores_table.at[location, "score"])
            print("\n" + "\n" + "Name: " + name + "\n" +
                "Student Number: " + str(stdnum) + "\n" +
                "Score: " + score + "\n" + "\n")
        else:
            print("\n" + "\n" + str(stdnum) + " is not found in the score file" + "\n" + "\n")
    else:
        print("\n" + "\n" + "Sorry, no quizzes have been attempted yet for " + course + "\n" + "\n")


def set_student_scores(course, student_number, score):
    """
    Modify student score if an error in quiz is present
    
    It modifies the student's score if there is an error in the quiz.
    
    Parameters
    ----------
    string : course
        course code
    string : student_number
        student number of the student
    string : score
        score of the student which needs to be updated
    """
    filename = SCORE_FILE_DIRECTORY + course + UNDERSCORE + SCORES + ".csv"
    if os.path.exists(filename):
        scores_table = pd.read_csv(filename, skipinitialspace = True)
        stdnum_list = list(scores_table["student_number"])
        if student_number in stdnum_list:
            if 0 <= score <= 100:
                scores_table.loc[scores_table.student_number == student_number, "score"] = score
                location = np.where(scores_table["student_number"] == student_number)[0][0]
                name = scores_table.at[location, "student_name"]
                print("\n" + "\n" + "updated mark for " + name + ": " + str(score) + "\n" + "\n")
                scores_table.to_csv(filename, index = False)
            else:
                print("Updated mark must be between 0 and 100 percent")
        else:
            print("\n" + "\n" + str(student_number) + " is not found in the score file" "\n" + "\n")
    else:
        print("\n" + "\n" + "Sorry, no quizzes have been attempted yet for " + course + "\n" + "\n")


def quiz_score_statistics(course):
    """
    Calculate and display average course grade of all students
    
    It calculates and display metrics like average, minimum, maximum etc.
    for the course grade of all students.
    
    Parameters
    ----------
    string : course
        course code
    """
    filename = SCORE_FILE_DIRECTORY + course + UNDERSCORE + SCORES + ".csv"
    if os.path.exists(filename):
        scores_table = pd.read_csv(filename, skipinitialspace = True)
        scores = scores_table["score"]
        minimum = str(min(scores))
        lowerQuartile = str(scores.quantile([0.25])).split()[1]
        average = str(stats.mean(scores))
        median = str(stats.median(scores))
        upperQuartile = str(scores.quantile([0.75])).split()[1]
        maximum = str(max(scores))
        print("\n" + "\n" +"MINIMUM: " + minimum + "\n" +
            "LOWER QUARTILE: " + lowerQuartile + "\n" +
            "MEAN: " + average + "\n" +
            "MEDIAN: " + median + "\n" +
            "UPPER QUARTILE: " + upperQuartile + "\n" +
            "MAXIMUM: " + maximum + "\n" + "\n")
    else:
        print("Sorry, no quizzes have been appempted yet for " + course)


def score_driver():
    """
    Driver code directing teacher to view a students mark,
    modify a students mark, calculate quiz summary statistics, or leave the program
    """
    while True:
        print("What would you like to do?")
        print("1. View students quiz mark \n2. Change a students quiz mark \n3. Calculate quiz score summary statistics \n4. Quit")
        response = input("response: ")
        match response:
            case "1":
                course = input("Provide the course code: ")
                stnum = int(input("Provide student number: "))
                get_student_scores(course, stnum)
            case "2": 
                course = input("Provide the course code: ")
                stnum = int(input("Provide student number: ")) 
                mark = int(input("Provide updated mark: "))
                set_student_scores(course, stnum, mark)
            case "3":
                course = input("Provide the course code: ")
                quiz_score_statistics(course)
            case "4":
                break
            case _:
                print("invalid option")


def quiz_or_score():
    """ 
    Driver code directing teacher to create a quiz,
    check quiz score marks, or leave the program
    """
    while True:
        print("Do you want to create a quiz or check quiz score marks?")
        print("1. Create Quiz \n2. See marks \n3. Quit")
        response = input("response: ")
        match response:
            case "1":
                cq.create_quiz()
            case "2":
                score_driver()
            case "3":
                break
            case _:
                print("Please enter valid input")