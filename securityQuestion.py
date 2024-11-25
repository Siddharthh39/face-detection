import json
import os
from tkinter import simpledialog, messagebox

questions_file = "face_data/security_questions.json"

# Function to prompt user for security questions during registration
def set_security_questions():
    questions = []
    answers = []

    # Ask for two security questions
    for i in range(2):
        question = simpledialog.askstring("Security Question", f"Enter security question {i + 1}:")
        answer = simpledialog.askstring("Answer", f"Enter the answer for question {i + 1}:", show="*")

        if question and answer:
            questions.append(question)
            answers.append(answer.lower())  # Save the answer in lowercase for consistency
        else:
            messagebox.showerror("Error", "Both question and answer must be provided.")
            return None, None

    # Save questions and answers to a file
    data = {"questions": questions, "answers": answers}
    with open(questions_file, "w") as file:
        json.dump(data, file)

    return questions, answers

# Function to verify security questions during access
def verify_security_questions():
    if not os.path.exists(questions_file):
        messagebox.showerror("Error", "No security questions found. Access denied.")
        return False

    # Load questions and answers
    with open(questions_file, "r") as file:
        data = json.load(file)

    questions = data["questions"]
    stored_answers = data["answers"]

    # Ask the user to answer the security questions
    for i, question in enumerate(questions):
        user_answer = simpledialog.askstring("Security Question", question, show="*")
        if not user_answer or user_answer.lower() != stored_answers[i]:
            messagebox.showerror("Error", "Incorrect answer. Access denied.")
            return False

    return True
