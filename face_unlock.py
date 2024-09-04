import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox, simpledialog

# Initialize the face detector
# For Linux
face_cap = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
# For Windows
face_cap = cv2.CascadeClassifier("C:/Users/singh/AppData/Roaming/Python/Python38/site-packages/cv2/data/haarcascade_frontalface_default.xml")
video_cap = cv2.VideoCapture(0)

# Path to the authorized face image
authorized_face_path = "face_data/authorized_face.jpg"
authorized_face = cv2.imread(authorized_face_path, cv2.IMREAD_GRAYSCALE)

# Load the credentials
with open("face_data/credentials.txt", "r") as cred_file:
    stored_security_code, stored_password = cred_file.read().splitlines()

# Function to verify security code and password
def verify_credentials():
    tries = 3
    while tries > 0:
        security_code = simpledialog.askstring("Security Code", "Enter your 5-digit security code:", parent=root)
        if len(security_code) != 5:
            messagebox.showerror("Error", "The security code must be exactly 5 digits.")
            continue

        password = simpledialog.askstring("Password", "Enter your password:", parent=root, show="*")
        if len(password) < 5:
            messagebox.showerror("Error", "The password must be at least 5 characters.")
            continue

        if security_code == stored_security_code and password == stored_password:
            return True
        else:
            tries -= 1
            messagebox.showerror("Error", f"Invalid credentials. {tries} tries left.")
    
    return False

# Start Tkinter root window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Verify credentials
if not verify_credentials():
    messagebox.showerror("Error", "Tries exhausted. Access denied.")
    exit()

# Proceed with face unlock
print("Starting face recognition... Position your face and press 's' to start recognition.")
while True:
    ret, frame = video_cap.read()
    if not ret:
        print("Error: Failed to capture image.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cap.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

    if len(faces) > 0:
        closest_face = max(faces, key=lambda face: face[2])
        (x, y, w, h) = closest_face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "Press 's' to recognize", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    cv2.imshow("Face Unlock", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s') and len(faces) > 0:
        face_data = gray[y:y + h, x:x + w]
        similarity = cv2.matchTemplate(face_data, authorized_face, cv2.TM_CCOEFF_NORMED)
        
        if np.max(similarity) > 0.7:
            messagebox.showinfo("Access Granted", "Welcome, User!")
            print("Face recognized. Welcome, User!")
            break
        else:
            messagebox.showerror("Access Denied", "Face not recognized.")
    
    if key == ord('a'):
        break

video_cap.release()
cv2.destroyAllWindows()
