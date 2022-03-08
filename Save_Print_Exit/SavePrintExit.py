import cv2, time, math
import HandTrackingModule as htm
import pyautogui as p

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0

detector = htm.handDetector(detectionCon=0.75)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        a, b = lmList[17][1], lmList[17][2]
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[2][1], lmList[2][2]
        len_thumbtip_pinky = math.hypot(x1-a, y1-b)
        len_thumbcmc_pinky = math.hypot(x2-a, y2-b)
        time.sleep(1)

        if ((lmList[4][2]<lmList[1][2]) and (lmList[4][2]<lmList[6][2]) and (lmList[4][2]<lmList[10][2]) and (lmList[4][2]<lmList[14][2])):
            print("[PRINT]") # 🤙 (Thumb up and pinky finger down)
            time.sleep(1)
            tab_count = 2
            p.keyDown('alt')
            for i in range(tab_count):
                p.press('tab')
            p.keyUp('alt')
            p.hotkey('ctrl', 's')
            p.hotkey('ctrl', 'p')
            time.sleep(2)

        elif (lmList[8][2]<lmList[6][2]) and (lmList[12][2]<lmList[10][2]) and (lmList[16][2]>lmList[14][2]) and (lmList[20][2]>lmList[18][2]) and (len_thumbtip_pinky<len_thumbcmc_pinky) and lmList[8][1]>lmList[12][1]:
            print("[SAVE]") # ✌️ (Only index n middle finger open)
            tab_count = 2
            p.keyDown('alt')
            for i in range(tab_count):
                p.press('tab')
            p.keyUp('alt')
            p.hotkey('ctrl', 's')
            p.keyDown('alt')
            for i in range(tab_count):
                p.press('tab')
            p.keyUp('alt')
            p.keyDown('alt')
            for i in range(tab_count):
                p.press('tab')
            p.keyUp('alt')

        elif (lmList[3][2]<lmList[4][2]):
            print("[EXIT]") # 👎 (Thumb down)
            tab_count = 2
            p.keyDown('alt')
            for i in range(tab_count):
                p.press('tab')
            p.keyUp('alt')
            p.hotkey('ctrl', 's')
            p.hotkey('alt', 'f4')

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (400,70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

