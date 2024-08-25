import cv2
import os

# Initialize the face detector
face_cap = cv2.CascadeClassifier("C:/Users/singh/AppData/Roaming/Python/Python38/site-packages/cv2/data/haarcascade_frontalface_default.xml")
video_cap = cv2.VideoCapture(0)

# Directory to save the face data
face_data_dir = "face_data"
if not os.path.exists(face_data_dir):
    os.makedirs(face_data_dir)

print("Position your face in front of the camera to register.")
face_registered = False

while True:
    ret, frame = video_cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cap.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        face_data = gray[y:y+h, x:x+w]
        cv2.imwrite(f"{face_data_dir}/authorized_face.jpg", face_data)
        face_registered = True
        break

    cv2.imshow("Register Face", frame)
    if cv2.waitKey(10) == ord("a") or face_registered:
        break

video_cap.release()
cv2.destroyAllWindows()

if face_registered:
    print("Face registration complete. You can now use face unlock.")
