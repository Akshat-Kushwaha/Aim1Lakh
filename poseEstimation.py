import cv2 as cv
import mediapipe as mp
import time
mpPose = mp.solutions.pose
pose = mpPose.Pose()
cap = cv.VideoCapture(0)
ptime = 0
mpDraw = mp.solutions.drawing_utils

while True:
    success,frame = cap.read()
    imgRgb = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
    result = pose.process(imgRgb)
    print(result.pose_landmarks)
    if result.pose_landmarks:
        mpDraw.draw_landmarks(frame,result.pose_landmarks,mpPose.POSE_CONNECTIONS)
        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime = ctime
        cv.putText(frame,str( round(fps) ),(70,60),cv.FONT_ITALIC,3,(255,0,255),5 )
        for id,lm in enumerate(result.pose_landmarks.landmark):
            h,w,c = frame.shape
            cx,cy = int(lm.x*w),int(lm.y*h)
            cv.circle(frame,(cx,cy),10,(255,0,255),-1)
    cv.imshow('video',frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break