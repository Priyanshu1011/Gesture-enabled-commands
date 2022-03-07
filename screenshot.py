
import cv2
import mediapipe as mp

img_counter=0
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
# For taking input using webcam
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.5,min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        l=[]
        success, image = cap.read()

        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue


        #convert the image BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image_height, image_width, _ = image.shape
        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                '''print(
                    f'mid: (',
                    f'{hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * image_width}, '
                    f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
                )'''
                fin=''
                if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y:
                    val1 = 0

                else:
                    val1 = 1
                    fin ='Index finger '
                    fgs =' '

                if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y:
                    val2 = 0
                else:
                    val2 = 1
                    fin += 'Middle finger '
                    fgs +=' '

                if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y:
                    val3 = 0
                else:
                    val3 = 1
                    fin += 'Ring finger '
                    fgs +='screenshot'


                val=val1 +val2+val3
                print(val)
                if val==3:    #screenshot will be taken only if 3 fingers are shown on webcam

                    l.append(1)




                fps= str(val)+' fingers'

                cv2.putText(image, (fps), (0, 25), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 3)
                cv2.putText(image, (fin), (0, 60), cv2.FONT_HERSHEY_PLAIN, 2, (10, 0, 0), 2)
                cv2.putText(image, (fgs), (0, 90), cv2.FONT_HERSHEY_TRIPLEX, 1, (180,10,0), 1)

        if len(l)==1:
            #for taking a screenshot
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, image)
            print("{} written!".format(img_name))


        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == ord('e'):
            break

cap.release()