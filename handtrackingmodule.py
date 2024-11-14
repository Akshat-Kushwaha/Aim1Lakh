import cv2 as cv
import mediapipe as mp
import time


class HandDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        # Initialize the MediaPipe Hands module for hand detection and tracking.
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils  # Drawing utilities to draw landmarks on images
        self.ptime = 0  # Previous time for FPS calculation

    def findHands(self, image, draw=True):
        """Detects hands in an image and optionally draws landmarks."""
        imgRGB = cv.cvtColor(image, cv.COLOR_BGR2RGB)  # Convert BGR to RGB
        self.results = self.hands.process(imgRGB)  # Process the RGB frame to detect hands
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image

    def findPosition(self, image, handNo=0, draw=True):
        """Finds and returns landmark positions in the image for a given hand."""
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw and id == 1:  # Draw a circle on landmark 1 as an example
                    cv.circle(image, (cx, cy), 25, (0, 255, 255), -1)
        return lmList

    def calculateFPS(self):
        """Calculates and returns frames per second (FPS) for real-time display."""
        ctime = time.time()
        fps = 1 / (ctime - self.ptime)
        self.ptime = ctime
        return fps


def main():
    cap = cv.VideoCapture(0)  # Start video capture from the default webcam
    detector = HandDetector()  # Create an instance of the HandDetector class

    while True:
        success, image = cap.read()  # Read a frame from the webcam
        if not success:
            break

        # Detect hands and landmarks
        image = detector.findHands(image)
        lmList = detector.findPosition(image)

        # Calculate FPS and display it
        fps = detector.calculateFPS()
        cv.putText(image, f'FPS: {int(fps)}', (30, 70), cv.FONT_ITALIC, 3, (255, 0, 255), 3)

        # Display the frame with hand landmarks in a window named 'hand'
        cv.imshow('hand', image)
        if (len(lmList) != 0):
            print(lmList[4])
        # Press 'q' to exit
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()