import cv2
import mediapipe as mp
import os
def cameravision():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 30)
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils
    try:
        while 1:
            font = cv2.FONT_HERSHEY_SIMPLEX
            ret, frame = cap.read()
            handsFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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
                    indexMid = 0
                    handBottomX = 0
                    handBottomY = 0
                    pinkyX = 0
                    pinkyY = 0
                    fistWarning = "Fist!"
                    for lms in lmList:
                        if lms[0] == 7:
                            indexX, indexY = lms[1], lms[2]
                        elif lms[0] == 5:
                            indexMid = lms[2]
                        elif lms[0] == 19:
                            pinkyX, pinkyY = lms[1], lms[2]
                        elif lms[0] == 0:
                            handBottomX, handBottomY = lms[1], lms[2]
                    if (indexY < handBottomY) and (indexY > indexMid):
                        cv2.rectangle(handsFrame, (indexX, indexY), (pinkyX, handBottomY), (0, 0, 255), 2)
                        cv2.putText(handsFrame, fistWarning, (pinkyX + 2, indexY - 2), (font), .7,
                                    (0, 0, 255), 1, cv2.LINE_4)
                        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                        cv2.destroyAllWindows() #sleepcmd
                        quit()
            cv2.imshow("Fist Detector", handsFrame)
            k = cv2.waitKey(10) & 0xFF
            #  1 is the escape key
            if k == "q":
                break
            else:
                pass
        cap.release()
    except cv2.error as e:
        print(str(e))
cameravision()
