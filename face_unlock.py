import cv2
import numpy as np
import subprocess
import userData  # Import userData for credential handling

# Initialize the face detector
face_cap = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
video_cap = cv2.VideoCapture(0)

if not video_cap.isOpened():
    print("Error: Could not open video capture.")
    exit()

# Load the registered face
authorized_face_path = "face_data/authorized_face.jpg"
authorized_face = cv2.imread(authorized_face_path, cv2.IMREAD_GRAYSCALE)
if authorized_face is None:
    print("No authorized face found. Please register a face first.")
    exit()

def recognize_face(face_data):
    result = cv2.matchTemplate(face_data, authorized_face, cv2.TM_CCOEFF_NORMED)
    return np.max(result)

# Load saved credentials
credentials = userData.load_credentials()
if not credentials:
    print("No credentials found. Please register a user first.")
    exit()

# Prompt the user for the security code and password
attempts = 3
while attempts > 0:
    entered_code = input("Enter your 5-digit security code: ")
    entered_password = input("Enter your password: ")

    if entered_code == credentials["security_code"] and entered_password == credentials["password"]:
        print("Credentials matched. Starting face recognition...")
        break
    else:
        attempts -= 1
        print(f"Incorrect credentials. {attempts} attempts remaining.")

    if attempts == 0:
        print("Tries exhausted. Access denied.")
        exit()

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
        similarity = recognize_face(face_data)

        if similarity > 0.7:
            cv2.putText(frame, "Welcome, User!", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            print("Face recognized. Welcome, User!")
            cv2.imshow("Face Unlock", frame)
            cv2.waitKey(2000)
            subprocess.Popen(["python3", "logIN.py"])
            break
        else:
            cv2.putText(frame, "Unauthorized", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            print("Face not recognized.")
            cv2.imshow("Face Unlock", frame)
            cv2.waitKey(2000)

    if key == ord('a'):
        break

video_cap.release()
cv2.destroyAllWindows()
