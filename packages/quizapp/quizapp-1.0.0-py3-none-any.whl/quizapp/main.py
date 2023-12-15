from student import takequiz as tq
from teacher import checkstudentscores as css

def start():
    print("Are you a student or a professor?")
    print("1. Student \n2. Teacher")
    role = input("Enter response:")

    match role:
        case "1":
            tq.select_quiz()
        case "2":
            css.quiz_or_score()
        case _ :
            print("Please enter valid input")     
