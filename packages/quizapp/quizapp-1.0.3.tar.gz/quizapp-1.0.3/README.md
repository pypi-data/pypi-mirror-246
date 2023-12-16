# Quizapp [![Build Status](https://app.travis-ci.com/somyanagar/quizapp_CI.svg?token=sKjZRvdQKxwyb9aZ9WVW&branch=main)](https://app.travis-ci.com/somyanagar/quizapp_CI)

The quizzing app is an interactive application that enables teachers to create and manage quizzes, and students to take each quiz. Each quiz must be multiple choice and contain a single answer. Upon quiz completion, students can view their quiz score and score averaged across all quizzes. Teachers can view all student quiz scores. Some features of quizapp include:

1.  The student selecting which course they want to take a quiz for.
2.  Saving the students score for each quiz and storing in a file for a given course.
3.  Outputting the student's average quiz score of all quizzes taken by a given student to the screen.
4.  Teachers can create new quizzes.
5.  Teachers can view and modify student quiz scores.
6.  Teachers can calculate and display overall quiz statistics for any course

#### Project Structure

<img src="assets/images/project_structure.png" width="200" height="253"/>

Main package name is **quizapp**. It contains a **main.py** module and two sub-packages: **student** and **teacher**. The student sub-package contains two modules: **readquiz.py** and **takequiz.py**. The teacher sub-package contains two modules: **createquiz.py** and **checkstudentscores.py**. There is an assets directory which contains data files for quizzes and scores.

#### student sub-package

The student sub-package contains two modules to handle the flows that a student user will interact with:

1.  **readquiz.py:**

    This module involves reading individual quizzes, enabling student users to complete them. This is accomplished with 2 classes and 4 functions:

    1.  *class Quiz:* This consists of a quiz object with three attributes, the **name** (i.e. course code) of a quiz, the individual **problems** in a quiz, and the total **number of problems**.

    2.  *class Problem:* This consists of a problem object with three attributes, the **question** itself, the multiple choice **options** for a question, and the **answer**.

    3.  *read_quiz():* Individual quizzes stored as json files are outputted to the screen

    4.  *get_available_courses():* Lists all available quizzes students can take

    5.  *save_score():* Saves the score a student achieved into a csv file of student quiz scores

    6.  *get_percentage():* Converts a students quiz score into a percentage.

2.  **takequiz.py:**

    This module handles the flow of student users taking quizzes. This is accomplished with 1 classes and 3 functions:

    1.  *class Student:* This consists of a student object with two attributes, **student name** and **student number**
    2.  *student_handler():* Initializes a student's name and number into a Student class object
    3.  *start_quiz():* The function where a student actually completes the quiz
    4.  *select_quiz():* Displays all available quizzes then prompts a student to select a quiz to complete.

#### teacher sub-package

The teacher sub-package contains module to handle the flows that a user with teacher role will interact with. It contains two modules:

1.  **createquiz.py:**

    This module handles the workflow of creating a quiz through an interactive menu through which a teacher can add a quiz for a course. It achieves this using the following methods:

    1.  *create_quiz():* This serves as a driver function to create a quiz and then writes the quiz into a JSON file in the appropriate directory with the appropriate filename.
    2.  *questionInput():* Takes the user input for questions, options and the answer and creates an object for the same.
    3.  *create_score_csv():* Creates a template score file whenever a new quiz is added. After each student has taken the quiz, their score is saved to the file created using this method.
    4.  *convert_to_json():* Converts the quiz from a dictionary object to JSON object and writes object into a JSON file.

2.  **checkstudentscores.py:**

    This module handles the workflow of viewing the scores for the quiz by the teacher and also allows them to view other statistics like mean, minimum, maximum etc. It achieves this using the following methods:

    1.  *get_student_scores():* It displays the student's quiz score for a course by taking student number and course code as arguments.
    2.  *set_student_scores():* It modifies the student's score if there is an error in the quiz.
    3.  *quiz_score_statistics():* It calculates and display metrics like average, minimum, maximum etc. for the course grade of all students.
    4.  *score_driver():* This is the driver method allowing the teacher to view a students mark, modify a students mark, calculate quiz summary statistics, or leave the program.
    5.  *quiz_or_score():* This is the driver method directing teacher to create a quiz, check quiz score marks, or leave the program
