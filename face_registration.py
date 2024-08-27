import cv2
import os

# Initialize the face detector
'''for linux'''
face_cap = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
'''for windows'''
# face_cap = cv2.CascadeClassifier("C:/Users/singh/AppData/Roaming/Python/Python38/site-packages/cv2/data/haarcascade_frontalface_default.xml")
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
    faces = face_cap.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

    for (x, y, w, h) in faces:
        # Draw a rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Indicate to the user to press 's' to save the image
        cv2.putText(frame, "Press 's' to save", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        # If 's' is pressed, save the face data
        if cv2.waitKey(1) & 0xFF == ord('s'):
            face_data = gray[y:y+h, x:x+w]
            cv2.imwrite(f"{face_data_dir}/authorized_face.jpg", face_data)
            face_registered = True
            print("Face captured and saved.")
            break

    cv2.imshow("Register Face", frame)
    
    if face_registered:
        break

    # Press 'q' to quit without saving
    if cv2.waitKey(1) & 0xFF == ord('a'):
        break

video_cap.release()
cv2.destroyAllWindows()

if face_registered:
    print("Face registration complete. You can now use face unlock.")
else:
    print("Face registration canceled.")
