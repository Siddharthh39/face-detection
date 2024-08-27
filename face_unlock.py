import cv2
import numpy as np
import subprocess

# Initialize the face detector
face_cap = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")

# Initialize video capture
video_cap = cv2.VideoCapture(0)

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

# Variable to track recognition status
face_recognized = False

while True:
    ret, frame = video_cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces with a minimum size to ensure human faces are captured
    faces = face_cap.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

    for (x, y, w, h) in faces:
        # Draw a rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Indicate to the user to press 's' to start recognition
        cv2.putText(frame, "Press 's' to recognize", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        # Wait for the user to press 's' to start recognition
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('s'):
            face_data = gray[y:y+h, x:x+w]
            similarity = recognize_face(face_data)
            
            if similarity > 0.7:  
                cv2.putText(frame, "Welcome, User!", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                print("Face recognized. Welcome, User!")
                cv2.imshow("Face Unlock", frame)
                cv2.waitKey(2000)  # Pause for 2 seconds to display the result
                subprocess.Popen(["python3", "logIN.py"])  # Open the logged-in window
                face_recognized = True
                break  # Exit the loop after successful recognition
            else:
                cv2.putText(frame, "Unauthorized", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                print("Face not recognized.")
                cv2.imshow("Face Unlock", frame)
                cv2.waitKey(2000)  # Pause for 2 seconds to display the result
                face_recognized = False
                break  # Exit the loop after failed recognition

    cv2.imshow("Face Unlock", frame)

    # Handle exit condition
    if face_recognized or not face_recognized:
        break

    # Press 'q' to quit the recognition process
    if key == ord('q'):
        break

video_cap.release()
cv2.destroyAllWindows()
