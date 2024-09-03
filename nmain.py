import tkinter as tk
import subprocess
from PIL import Image, ImageTk  # Requires Pillow for image display
import cv2
import os

# Directory where the face data is stored
face_data_dir = "face_data"
authorized_face_path = f"{face_data_dir}/authorized_face.jpg"

# Function to display the registered face image for developer mode
def show_registered_image():
    if os.path.exists(authorized_face_path):
        img = Image.open(authorized_face_path)
        img = img.resize((200, 200), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        img_window = tk.Toplevel(root)
        img_window.title("Registered Face")
        img_label = tk.Label(img_window, image=img)
        img_label.image = img  # Keep a reference to avoid garbage collection
        img_label.pack(pady=10)
    else:
        tk.messagebox.showinfo("Info", "No registered face found.")

# Function to run the face registration script
def run_face_registration():
    subprocess.run(["python", "face_registration.py"])

# Function to run the face unlock script
def run_face_unlock():
    subprocess.run(["python", "face_unlock.py"])

# Placeholder function for security questions
def security_questions():
    tk.messagebox.showinfo("Security Questions", "Security questions are not implemented yet.")

# Developer Mode Interface
def developer_mode():
    dev_window = tk.Toplevel(root)
    dev_window.title("Developer Mode")
    dev_window.geometry("300x300")

    tk.Label(dev_window, text="Developer Mode", font=("Helvetica", 16)).pack(pady=10)

    # Buttons for developer mode actions
    tk.Button(dev_window, text="Show Registered Image", command=show_registered_image, width=25).pack(pady=5)
    tk.Button(dev_window, text="Face Registration", command=run_face_registration, width=25).pack(pady=5)
    tk.Button(dev_window, text="Face Unlock", command=run_face_unlock, width=25).pack(pady=5)
    tk.Button(dev_window, text="Security Questions", command=security_questions, width=25).pack(pady=5)

# Tester Mode Interface
def tester_mode():
    test_window = tk.Toplevel(root)
    test_window.title("Tester Mode")
    test_window.geometry("300x200")

    tk.Label(test_window, text="Tester Mode", font=("Helvetica", 16)).pack(pady=10)

    # Buttons for tester mode actions
    tk.Button(test_window, text="Unlock with Face", command=run_face_unlock, width=25).pack(pady=5)
    tk.Button(test_window, text="Security Questions", command=security_questions, width=25).pack(pady=5)

# Main application window
root = tk.Tk()
root.title("Face Unlock System - Main Menu")
root.geometry("300x150")

# Main menu buttons for selecting mode
tk.Button(root, text="Developer Mode", command=developer_mode, width=25, height=2).pack(pady=10)
tk.Button(root, text="Tester Mode", command=tester_mode, width=25, height=2).pack(pady=10)

# Start the Tkinter main loop
root.mainloop()
