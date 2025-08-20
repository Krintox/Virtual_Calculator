# main.py
import cv2
import mediapipe as mp
import time
import numpy as np

from keypad import build_keys, Key
from utils import point_in_rect, dist, draw_keys
from calc_engine import safe_eval, CalcError

# --- Configuration (tweakable) ---
PINCH_THRESHOLD_RATIO = 0.04   # fraction of frame width -> pinch threshold
DWELL_FRAMES = 12              # frames of dwell to trigger press
COOLDOWN_FRAMES = 12           # after a press, cooldown to avoid repeats

# --- Setup MediaPipe ---
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.6,
                       min_tracking_confidence=0.6)

cap = cv2.VideoCapture(0)
time.sleep(0.5)

keys = None
frame_w, frame_h = None, None

expression = ""
last_result = ""
dwell_counter = 0
last_highlight_label = None
cooldown = 0

def register_press(label: str):
    global expression, last_result
    if label == "C":
        expression = ""
        last_result = ""
    elif label == "=":
        try:
            val = safe_eval(expression) if expression.strip() != "" else ""
            if val == "":
                last_result = ""
            else:
                # format int if whole, else float
                if isinstance(val, float) and val.is_integer():
                    val = int(val)
                last_result = str(val)
                expression = str(val)  # show result as next input
        except CalcError:
            last_result = "ERROR"
            expression = ""
    else:
        # append digit / operator
        expression += label

print("Starting Virtual Air-Calculator. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed camera frame")
        break

    # mirror for natural interaction
    frame = cv2.flip(frame, 1)
    if frame_w is None or frame_h is None or keys is None:
        frame_h, frame_w = frame.shape[:2]
        keys = build_keys(frame_w, frame_h)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    # default visuals
    highlight_key = None
    pressed_key = None
    fingertip_pt = None
    pinch_detected = False

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        # get landmarks 8 (index fingertip) and 4 (thumb tip)
        lm = hand.landmark
        ix, iy = int(lm[8].x * frame_w), int(lm[8].y * frame_h)
        tx, ty = int(lm[4].x * frame_w), int(lm[4].y * frame_h)
        fingertip_pt = (ix, iy)

        # draw simple fingertip marker
        cv2.circle(frame, fingertip_pt, 8, (255, 0, 255), -1)

        # compute pinch distance
        pinch_px = dist((ix, iy), (tx, ty))
        pinch_thresh = max(12, int(frame_w * PINCH_THRESHOLD_RATIO))
        if pinch_px < pinch_thresh:
            pinch_detected = True
            # draw small line showing pinch
            cv2.line(frame, (ix, iy), (tx, ty), (0,255,0), 2)

        # find which key the fingertip is above (if any)
        current_key = None
        for k in keys:
            if point_in_rect(ix, iy, k):
                highlight_key = k
                current_key = k
                break

        # dwell logic
        if current_key is not None and current_key.label == last_highlight_label:
            dwell_counter += 1
        else:
            dwell_counter = 0

        last_highlight_label = current_key.label if current_key is not None else None

        # press detection: either pinch or dwell long enough, and cooldown is zero
        if cooldown == 0:
            if pinch_detected and current_key is not None:
                register_press(current_key.label)
                pressed_key = current_key
                cooldown = COOLDOWN_FRAMES
            elif dwell_counter >= DWELL_FRAMES and current_key is not None:
                register_press(current_key.label)
                pressed_key = current_key
                cooldown = COOLDOWN_FRAMES

        # (optional) draw full hand landmarks for debugging:
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    # draw keypad and highlights
    draw_keys(frame, keys, highlight=highlight_key, pressed=pressed_key)

    # show expression and result at top-left
    overlay_h = 80
    cv2.rectangle(frame, (10,10), (frame_w-10, 10+overlay_h), (40,40,40), -1)  # background
    cv2.putText(frame, f"Expr: {expression}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (240,240,240), 2)
    cv2.putText(frame, f"Result: {last_result}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200,200,255), 2)

    # show debug hints (small)
    cv2.putText(frame, "Pinch to press or hover for a moment", (20, frame_h-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (220,220,220), 1)

    cv2.imshow("Virtual Air-Calculator", frame)

    # cooldown decrement
    if cooldown > 0:
        cooldown -= 1

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('c'):
        expression = ""
        last_result = ""
    if key == ord('='):
        # manual keyboard evaluate
        try:
            val = safe_eval(expression) if expression.strip() != "" else ""
            if val == "":
                last_result = ""
            else:
                if isinstance(val, float) and val.is_integer():
                    val = int(val)
                last_result = str(val)
                expression = str(val)
        except Exception:
            last_result = "ERROR"
            expression = ""

cap.release()
cv2.destroyAllWindows()
