import cv2
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

# Initialize the face detector
# For Linux
face_cap = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
# For Windows
face_cap = cv2.CascadeClassifier("C:/Users/singh/AppData/Roaming/Python/Python38/site-packages/cv2/data/haarcascade_frontalface_default.xml")
video_cap = cv2.VideoCapture(0)

# Directory to save the face data
face_data_dir = "face_data"
if not os.path.exists(face_data_dir):
    os.makedirs(face_data_dir)

# Function to prompt the user for a 5-digit code and password
def prompt_for_credentials():
    while True:
        security_code = simpledialog.askstring("Security Code", "Enter a 5-digit security code:", parent=root)
        if len(security_code) != 5:
            messagebox.showerror("Error", "The security code must be exactly 5 digits.")
            continue

        password = simpledialog.askstring("Password", "Enter a password (at least 5 characters):", parent=root, show="*")
        if len(password) < 5:
            messagebox.showerror("Error", "The password must be at least 5 characters.")
            continue

        return security_code, password

# Start Tkinter root window
root = tk.Tk()
root.withdraw()  # Hide the root window

print("Position your face in front of the camera to register.")
face_registered = False

while True:
    ret, frame = video_cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cap.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

    if len(faces) > 0:
        closest_face = max(faces, key=lambda face: face[2])
        (x, y, w, h) = closest_face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "Press 's' to save", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    cv2.imshow("Register Face", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s') and len(faces) > 0:
        face_data = gray[y:y + h, x:x + w]
        cv2.imwrite(f"{face_data_dir}/authorized_face.jpg", face_data)
        face_registered = True
        print("Face captured and saved.")
        break

    if key == ord('a'):
        break

video_cap.release()
cv2.destroyAllWindows()

if face_registered:
    # Prompt for security code and password
    security_code, password = prompt_for_credentials()
    
    # Save the credentials to a file
    with open(f"{face_data_dir}/credentials.txt", "w") as cred_file:
        cred_file.write(f"{security_code}\n{password}")
    print("Face registration complete. You can now use face unlock.")
else:
    print("Face registration canceled.")
