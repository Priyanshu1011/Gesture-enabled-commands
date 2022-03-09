#hibernate #fist closed with thumb in
import cv2
import mediapipe as mp
import os
counter=0
def cameravision():
    cap = cv2.VideoCapture(0) #diff for mac
    cap.set(cv2.CAP_PROP_FPS, 30)
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils
    try:
        while 1:
            font = cv2.FONT_HERSHEY_SIMPLEX
            ret, frame = cap.read()
            handsFrame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            results = hands.process(handsFrame)
            if results.multi_hand_landmarks:
                for handLMS in results.multi_hand_landmarks:
                    lmList = []
                    for id, lm in enumerate(handLMS.landmark):
                        h, w, c = handsFrame.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lmList.append([id, cx, cy])
                    indexX = 0
                    indexY = 0
                    indexmid = 0
                    handBottomX = 0
                    handBottomY = 0
                    pinkyX = 0
                    pinkyY = 0
                    thumbx = 0
                    thumby= 0
                    thumbmid = 0
                    pext = "Fist!"
                    for lms in lmList:
                        if lms[0] == 7:
                            indexX, indexY = lms[1], lms[2]
                            #cv2.circle(handsFrame, (lms[1], lms[2]), 2, (255, 0, 255), cv2.FILLED)
                        elif lms[0] == 5:
                            indexmid = lms[2]
                            #cv2.circle(handsFrame, (lms[1], lms[2]), 2, (255, 0, 255), cv2.FILLED)
                        elif lms[0] == 11:
                            middlex,middleY = lms[1],lms[2]
                            #cv2.circle(handsFrame, (lms[1], lms[2]), 2, (255, 0, 255), cv2.FILLED)
                        elif lms[0] == 9:
                            midmid = lms[2]
                        elif lms[0] == 15:
                            ringx, ringY = lms[1],lms[2]
                            #cv2.circle(handsFrame, (lms[1], lms[2]), 2, (255, 0, 255), cv2.FILLED)
                        elif lms[0] == 13:
                            ringmid = lms[2]
                        elif lms[0] == 19:
                            pinkyX, pinkyY = lms[1], lms[2]
                            #cv2.circle(handsFrame, (lms[1], lms[2]), 2, (255, 0, 255), cv2.FILLED)
                        elif lms[0] == 17:
                            pinkymid = lms[2]
                        elif lms[0] == 0:
                            handBottomX, handBottomY = lms[1], lms[2]
                        elif lms[0] == 4:
                            thumbx,thumby = lms[1],lms[2]
                            #cv2.circle(handsFrame, (lms[1], lms[2]), 2, (255, 0, 255), cv2.FILLED)
                        elif lms[0] == 3:
                            thumbmid = lms[1]
                            #cv2.circle(handsFrame, (lms[1], lms[2]), 2, (255, 0, 255), cv2.FILLED)
                    if ((indexY < handBottomY) and (indexY > indexmid)) and ((middleY < handBottomY) and (middleY > midmid)) and ((ringY < handBottomY) and (ringY > ringmid)) and ((pinkyY < handBottomY) and (pinkyY > pinkymid)) and (thumbx <= thumbmid) :
                        global counter
                        cv2.rectangle(handsFrame, (indexX, indexY), (pinkyX, handBottomY), (0, 0, 255), 2)
                        cv2.putText(handsFrame, pext, (pinkyX + 2, indexY - 2), (font), .7,(0, 0, 255), 1, cv2.LINE_4)
                        counter+=1
                        if counter>3:
                            print("Fist Recognized")
                            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                            cv2.destroyAllWindows() #sleepcmd
                            quit()
            cv2.imshow("Fist Detector", handsFrame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
    except cv2.error as e:
        print(str(e))
cameravision()
