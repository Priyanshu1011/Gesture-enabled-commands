import cv2
import mediapipe as mp
from math import hypot
import screen_brightness_control as sbc  # for brightness control
import numpy as np 

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands 
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
    success,img = cap.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    lmList = []
    if results.multi_hand_landmarks:
        for handlandmark in results.multi_hand_landmarks:
            for id,lm in enumerate(handlandmark.landmark):
                h,w,_ = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy]) 
            mpDraw.draw_landmarks(img,handlandmark,mpHands.HAND_CONNECTIONS)
    
    if lmList != []:
        # coordinates for brightness control
        x1,y1 = lmList[4][1],lmList[4][2]
        x2,y2 = lmList[12][1],lmList[12][2]
        # Drawing circle and line for brightness control
        cv2.circle(img, (x1, y1), 4, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 4, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,0), 3)

        lengthBright = hypot(x2-x1,y2-y1)

        bright = np.interp(lengthBright,[30,350],[0,100])
        brightBar = np.interp(lengthBright, [30,350],[400,150])
        brightPer=np.interp(lengthBright, [30,350],[0,100])

        sbc.set_brightness(int(bright))

        #Brightness bar
        cv2.rectangle(img,(50,150),(85,400),(0,0,255),4) 
        cv2.rectangle(img,(50,int(brightBar)),(85,400),(0,0,255),cv2.FILLED)
        cv2.putText(img,f"{int(brightPer)}%",(10,40),cv2.FONT_ITALIC,1,(0, 255, 98),3)

    cv2.imshow('Image',img)
    if cv2.waitKey(1) & 0xff==ord('q'):
        break