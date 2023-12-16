import string
import pandas as pd
import json

# Constants
QUIZ_FILE_DIRECTORY = "../assets/quizzes/"
UNDERSCORE = '_'
SCORE_FILE_DIRECTORY = "../assets/scores/"
SCORES = 'scores'
q = ""
o = []
a = ""

class Question():
    """ This class bundles the quiz inputs into a dictionary"""
    all_questions = []

    def __init__(self, question, options, answer):
        self.quiz = {}
        self.question = question
        self.options = options
        self.answer = answer
    
    def write_to_dict(self):
        """ Create a dictionary from the question class attributes """
        self.quiz["question"] = self.question
        self.quiz["options"] = self.options
        self.quiz["answer"] = self.answer
        Question.all_questions.append(self.quiz)
        return Question.all_questions

class questionInput():
    """
    Provides user inputed quiz question, options, and answers to the Question class.
    
    Takes the user input for questions, options and the answer and creates an object for the same.
    
    Returns
    ----------
    list
        list of question, options and answer
    """
    def quiz_inputs(self):
        self.question = input("Input Question: ")
        self.options = []
        self.answer = ""
        self.answer_added = False
        num_options = 1
        for letter in string.ascii_uppercase:
            option = input(f"{letter}. Enter option: ")
            self.options.append(f"{letter}. {option}")
            if self.answer_added == False:
                print("Is this the correct answer? ('y' for yes, any other key for no)")
                response = input("RESPONSE: ")
                if response.lower() == "y":
                    self.answer = f"{letter}. {option}"
                    self.answer_added = True
            response = print("Would you like to input another option? ('y' for yes, any other key for no)")
            response = input("RESPONSE: ")
            if response.lower() != "y":
                break
            else:
                num_options += 1

        return [self.question, self.options, self.answer]
    
def convert_to_json(course, questions):
    """
    Converts quiz dictionary to json object and writes object into json file.
    
    Parameters
    ----------
    string : course
        course code
    list : questions
        quiz questions
    """ 
    filename = QUIZ_FILE_DIRECTORY + course + ".json"
    with open(filename, "w") as out_file:
        json.dump(questions, out_file, indent=6)  

def create_score_csv(course):
    """
    Create empty csv file to store all student quiz grades for a course.
    
    Parameters
    ----------
    string : course
        course code
    """ 
    filename = SCORE_FILE_DIRECTORY + course + UNDERSCORE + SCORES + ".csv"
    data = ["student_number", "student_name", "score"]
    df = pd.DataFrame(columns = data)
    df.to_csv(filename, index = False)

def create_quiz():
    """
    Driver function to create a quiz and write quiz into a file as a json object.
    
    This serves as adriver function to create a quiz and then
    writes the quiz into a JSON file in the appropriate directory
    with the appropriate filename.
    """ 

    print("Do you want to create a quiz?('y' for yes, any other key for no)")
    response = input("RESPONSE: ")
    if response.lower() == "y":
        while True:
            q_contents = questionInput().quiz_inputs()
            q = Question(q_contents[0], q_contents[1], q_contents[2])
            questions = q.write_to_dict()
            print("Do you want to add another question?")
            print("'y' for yes, any other key for no")
            response = input("response: ")
            if response.lower() != "y":
                break
        course = input("Input the course code: ")
        convert_to_json(course, questions)
        create_score_csv(course)
    else:
        print("Not creating quiz")


