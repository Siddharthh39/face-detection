import cv2
import numpy as np
import subprocess

# Initialize the face detector
face_cap = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")

# Initialize video capture
video_cap = cv2.VideoCapture(0)

# Check if the video capture device is opened
if not video_cap.isOpened():
    print("Error: Could not open video capture.")
    exit()

# Path to the authorized face image
authorized_face_path = "face_data/authorized_face.jpg"
authorized_face = cv2.imread(authorized_face_path, cv2.IMREAD_GRAYSCALE)

# Check if the authorized face image exists
if authorized_face is None:
    print("No authorized face found. Please register a face first.")
    exit()

def recognize_face(face_data):
    result = cv2.matchTemplate(face_data, authorized_face, cv2.TM_CCOEFF_NORMED)
    return np.max(result)

print("Starting face recognition... Position your face and press 's' to start recognition.")

while True:
    ret, frame = video_cap.read()
    if not ret:
        print("Error: Failed to capture image.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cap.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

    if len(faces) > 0:
        # Find the closest face by selecting the one with the maximum width
        closest_face = max(faces, key=lambda face: face[2])  # face[2] is the width of the face
        (x, y, w, h) = closest_face

        # Draw a rectangle around the closest face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "Press 's' to recognize", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    # Display the frame
    cv2.imshow("Face Unlock", frame)

    # Handle key presses
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s') and len(faces) > 0:
        # Use the closest face for recognition
        face_data = gray[y:y + h, x:x + w]
        similarity = recognize_face(face_data)

        if similarity > 0.7:
            cv2.putText(frame, "Welcome, User!", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            print("Face recognized. Welcome, User!")
            cv2.imshow("Face Unlock", frame)
            cv2.waitKey(2000)  # Pause for 2 seconds to display the result
            subprocess.Popen(["python3", "logIN.py"])  # Open the logged-in window
            break  # Exit the loop after successful recognition
        else:
            cv2.putText(frame, "Unauthorized", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            print("Face not recognized.")
            cv2.imshow("Face Unlock", frame)
            cv2.waitKey(2000)  # Pause for 2 seconds to display the result

    # Press 'q' to quit the recognition process
    if key == ord('a'):
        break

video_cap.release()
cv2.destroyAllWindows()
