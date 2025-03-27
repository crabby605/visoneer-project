import cv2
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

def recognize_gesture(landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]

    # Example Gesture: Index finger up, thumb up = Open Terminal
    if index_tip.y < landmarks[6].y and thumb_tip.y < landmarks[2].y:
        return "open_terminal"
    
    # Example Gesture: Thumb up = Open Browser
    if thumb_tip.y < landmarks[2].y and index_tip.y > landmarks[6].y:
        return "open_browser"

    return None

def perform_action(gesture):
    if gesture == "open_terminal":
        pyautogui.hotkey("ctrl", "alt", "t")  # Opens terminal
    elif gesture == "open_browser":
        pyautogui.hotkey("ctrl", "alt", "b")  # You can change this to open your browser

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)  # Flip the image for mirror effect
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesture = recognize_gesture(hand_landmarks.landmark)
            if gesture:
                perform_action(gesture)

    cv2.imshow("Gesture Control", frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
