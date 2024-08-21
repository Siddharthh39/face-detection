import cv2

# Load the pre-trained face detection model from OpenCV's data directory.
face_cap = cv2.CascadeClassifier("C:/Users/singh/AppData/Roaming/Python/Python38/site-packages/cv2/data/haarcascade_frontalface_default.xml")

# Start capturing video from the default webcam (0 refers to the default camera).
video_cap = cv2.VideoCapture(0)

# Enter an infinite loop to process the video frame by frame.
while True:
    # Capture a single frame of video. 'ret' is a boolean that indicates if the frame was captured successfully.
    ret, video_data = video_cap.read()
    
    # Convert the captured frame to grayscale. Face detection typically works better on grayscale images.
    col = cv2.cvtColor(video_data, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the grayscale image. This function returns a list of rectangles where faces are detected.
    faces = face_cap.detectMultiScale(
        col,                   # The input image in grayscale.
        scaleFactor=1.1,       # The factor by which the image size is reduced at each image scale.
        minNeighbors=5,        # The number of neighbors each rectangle should have to retain it.
        minSize=(30, 30),      # The minimum possible object size (faces smaller than this are ignored).
        flags=cv2.CASCADE_SCALE_IMAGE  # The flag used to indicate the method of scaling the image.
    )
    
    # Loop through the list of detected faces.
    for (x, y, w, h) in faces:
        # Draw a rectangle around each detected face in the original (colored) video frame.
        cv2.rectangle(video_data, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Display the current frame with the rectangles drawn around detected faces.
    cv2.imshow("video_live", video_data)
    
    # Wait for 10 milliseconds for a key press. If the key 'a' is pressed, exit the loop and stop the video capture.
    if cv2.waitKey(10) == ord("a"):
        break

# Release the webcam resource. This is important to free up the camera for other applications.
video_cap.release()
def new():
    pass