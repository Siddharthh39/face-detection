import cv2
import os
import userData  # Import the new userData module for handling credentials

# Initialize the face detector
face_cap = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
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

    if len(faces) > 0:
        closest_face = max(faces, key=lambda face: face[2])  # Find the closest face
        (x, y, w, h) = closest_face

        # Draw a rectangle around the closest face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "Press 's' to save", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    cv2.imshow("Register Face", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s') and len(faces) > 0:
        # Save the closest face data
        face_data = gray[y:y + h, x:x + w]
        cv2.imwrite(f"{face_data_dir}/authorized_face.jpg", face_data)
        face_registered = True
        print("Face captured and saved.")
        stop_requested = True

    elif key == ord('a'):
        stop_requested = True

    if stop_requested:
        break

video_cap.release()
cv2.destroyAllWindows()

if face_registered:
    # Prompt the developer to enter a 5-digit code and password
    print("Please enter a 5-digit security code:")
    security_code = input("> ")

    print("Please enter a password:")
    password = input("> ")

    # Save the credentials using userData
    userData.save_credentials(security_code, password)
    print("Registration complete. You can now use face unlock.")
else:
    print("Face registration canceled.")
