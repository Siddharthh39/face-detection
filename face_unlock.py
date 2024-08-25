import cv2
import numpy as np

# Load the face detector and the authorized face
face_cap = cv2.CascadeClassifier("C:/Users/singh/AppData/Roaming/Python/Python38/site-packages/cv2/data/haarcascade_frontalface_default.xml")
video_cap = cv2.VideoCapture(0)
authorized_face_path = "face_data/authorized_face.jpg"
authorized_face = cv2.imread(authorized_face_path, cv2.IMREAD_GRAYSCALE)

if authorized_face is None:
    print("No authorized face found. Please register a face first.")
    exit()

def recognize_face(face_data):
    result = cv2.matchTemplate(face_data, authorized_face, cv2.TM_CCOEFF_NORMED)
    return np.max(result)

print("Starting face recognition...")

while True:
    ret, frame = video_cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cap.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        face_data = gray[y:y+h, x:x+w]
        similarity = recognize_face(face_data)
        
        if similarity > 0.7:  # Adjust threshold as needed
            cv2.putText(frame, "Welcome, User!", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            print("Face recognized. Welcome, User!")
        else:
            cv2.putText(frame, "Unauthorized", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            print("Face not recognized.")

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Face Unlock", frame)
    if cv2.waitKey(10) == ord("a"):
        break

video_cap.release()
cv2.destroyAllWindows()
