import tkinter as tk
import subprocess

# Function to run the face registration script
def record_face_data():
    subprocess.run(["python", "face_registration.py"])

# Function to run the face unlock script
def verify_face_data():
    subprocess.run(["python", "face_unlock.py"])

# Create the main window
root = tk.Tk()
root.title("Face Unlock System")

# Set the size of the window
root.geometry("300x150")

# Create buttons for the two options
record_button = tk.Button(root, text="Record New Face Data", command=record_face_data, width=25, height=2)
record_button.pack(pady=10)

verify_button = tk.Button(root, text="Verify Face Data", command=verify_face_data, width=25, height=2)
verify_button.pack(pady=10)

# Start the Tkinter main loop
root.mainloop()
