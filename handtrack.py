from time import ctime

import cv2
import cv2 as cv  # Import OpenCV library as 'cv' for image processing tasks.
import mediapipe as mp  # Import MediaPipe library as 'mp' for using pre-trained models.
import time  # Import time module to track time (optional, not used in this code).

# Start video capture from the default webcam (device index 0).
cap = cv.VideoCapture(0)

# Initialize the MediaPipe Hands module for hand detection and tracking.
mpHands = mp.solutions.hands
hands = mpHands.Hands()  # Create an instance of the Hands class to detect hand landmarks.
mpDraw = mp.solutions.drawing_utils  # Initialize drawing utilities to draw landmarks on images.

# Start an infinite loop to continuously read frames from the webcam.
ptime = 0
while True:
    success, image = cap.read()  # Read a frame from the webcam.
    if not success:  # If no frame is captured (e.g., webcam not available), break out of the loop.
        break

    # Convert the captured frame from BGR color space (used by OpenCV) to RGB.
    imgRGB = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    # Process the RGB frame to detect hands and landmarks.
    results = hands.process(imgRGB)

    # Check if any hand landmarks were detected.
    if results.multi_hand_landmarks:
        # Loop over each detected hand's landmarks.
        for handLms in results.multi_hand_landmarks:
            # Draw landmarks and connections on the original BGR frame.
            mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)
            for id,lm in enumerate(handLms.landmark):
                h,w,c = image.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                if (id == 1):
                    cv.circle(image,(cx,cy),25,(0,255,255),-1)
    # Display the frame with hand landmarks in a window named 'hand'.
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv.putText( image,str( round(fps) ) ,(30,70),cv2.FONT_ITALIC,3,(255,0,255),3)
    cv.imshow('hand', image)
    # Check if 'q' key is pressed to exit the loop.
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows.
cap.release()
cv.destroyAllWindows()
