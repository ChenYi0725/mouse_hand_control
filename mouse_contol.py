import pyautogui
import cv2
import mediapipe as mp
import random

mp_drawing = mp.solutions.drawing_utils  # mediapipe 繪圖方法
mp_drawing_styles = mp.solutions.drawing_styles  # mediapipe 繪圖樣式
mp_hands = mp.solutions.hands  # mediapipe 偵測手掌方法

cap = cv2.VideoCapture(0)
x = 100
y = 100
# mediapipe 啟用偵測手掌
with mp_hands.Hands(
    model_complexity=0,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
) as hands:

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        ret, image = cap.read()
        if not ret:
            print("Cannot receive frame")
            break
        image = cv2.flip(image, 1)
        size = image.shape  # 取得攝影機影像尺寸
        w = pyautogui.size().width  # 取得畫面寬度
        h = pyautogui.size().height  # 取得畫面高度

        image2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 將 BGR 轉換成 RGB
        results = hands.process(image2)  # 偵測手掌

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                x = hand_landmarks.landmark[7].x * w * 1.5  # 食指x
                y = hand_landmarks.landmark[7].y * h * 1.5  # 食指y

                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style(),
                )  # 畫手掌

        x = pyautogui.position().x
        y = pyautogui.position().y
        pyautogui.moveTo(x, y)

cap.release()
cv2.destroyAllWindows()
