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
stop_requested = False

while True:
    ret, frame = video_cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cap.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, "Press 's' to save", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    # Display the frame
    cv2.imshow("Register Face", frame)
    
    # Handle key press
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s') and len(faces) > 0:
        # Save the face data if 's' is pressed and a face is detected
        (x, y, w, h) = faces[0]  # Use the first detected face
        face_data = gray[y:y+h, x:x+w]
        cv2.imwrite(f"{face_data_dir}/authorized_face.jpg", face_data)
        face_registered = True
        print("Face captured and saved.")
        stop_requested = True

    elif key == ord('a'):
        # Stop the loop if 'a' is pressed
        stop_requested = True

    if stop_requested:
        break

video_cap.release()
cv2.destroyAllWindows()

if face_registered:
    print("Face registration complete. You can now use face unlock.")
else:
    print("Face registration canceled.")
