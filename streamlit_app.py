# streamlit_app.py
import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import time

from keypad import build_keys
from utils import point_in_rect, dist, draw_keys
from calc_engine import safe_eval, CalcError

# --- Config ---
PINCH_THRESHOLD_RATIO = 0.04
DWELL_FRAMES = 12
COOLDOWN_FRAMES = 12

# Mediapipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6,
)

# Session state for calculator
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "last_result" not in st.session_state:
    st.session_state.last_result = ""
if "cooldown" not in st.session_state:
    st.session_state.cooldown = 0
if "dwell_counter" not in st.session_state:
    st.session_state.dwell_counter = 0
if "last_highlight_label" not in st.session_state:
    st.session_state.last_highlight_label = None

def register_press(label: str):
    if label == "C":
        st.session_state.expression = ""
        st.session_state.last_result = ""
    elif label == "=":
        try:
            val = safe_eval(st.session_state.expression) if st.session_state.expression.strip() != "" else ""
            if val == "":
                st.session_state.last_result = ""
            else:
                if isinstance(val, float) and val.is_integer():
                    val = int(val)
                st.session_state.last_result = str(val)
                st.session_state.expression = str(val)
        except CalcError:
            st.session_state.last_result = "ERROR"
            st.session_state.expression = ""
    else:
        st.session_state.expression += label

# --- Streamlit Layout ---
st.title("🖐️ Virtual Air Calculator")
st.markdown("Move your finger over keys on the right and pinch to press.")

FRAME_WINDOW = st.image([])  # Placeholder for webcam frames

cap = cv2.VideoCapture(0)
frame_w, frame_h = None, None
keys = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        st.write("Camera not detected.")
        break

    frame = cv2.flip(frame, 1)
    if frame_w is None or frame_h is None:
        frame_h, frame_w = frame.shape[:2]
        keys = build_keys(frame_w, frame_h)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    highlight_key = None
    pressed_key = None

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        lm = hand.landmark
        ix, iy = int(lm[8].x * frame_w), int(lm[8].y * frame_h)  # index finger tip
        tx, ty = int(lm[4].x * frame_w), int(lm[4].y * frame_h)  # thumb tip

        cv2.circle(frame, (ix, iy), 8, (255, 0, 255), -1)

        pinch_px = dist((ix, iy), (tx, ty))
        pinch_thresh = max(12, int(frame_w * PINCH_THRESHOLD_RATIO))
        pinch_detected = pinch_px < pinch_thresh
        if pinch_detected:
            cv2.line(frame, (ix, iy), (tx, ty), (0,255,0), 2)

        current_key = None
        for k in keys:
            if point_in_rect(ix, iy, k):
                highlight_key = k
                current_key = k
                break

        # dwell counter
        if current_key and current_key.label == st.session_state.last_highlight_label:
            st.session_state.dwell_counter += 1
        else:
            st.session_state.dwell_counter = 0
        st.session_state.last_highlight_label = current_key.label if current_key else None

        if st.session_state.cooldown == 0:
            if pinch_detected and current_key:
                register_press(current_key.label)
                pressed_key = current_key
                st.session_state.cooldown = COOLDOWN_FRAMES
            elif st.session_state.dwell_counter >= DWELL_FRAMES and current_key:
                register_press(current_key.label)
                pressed_key = current_key
                st.session_state.cooldown = COOLDOWN_FRAMES

        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    draw_keys(frame, keys, highlight=highlight_key, pressed=pressed_key)

    # overlays
    cv2.rectangle(frame, (10,10), (frame_w-10, 90), (40,40,40), -1)
    cv2.putText(frame, f"Expr: {st.session_state.expression}", (20, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (240,240,240), 2)
    cv2.putText(frame, f"Result: {st.session_state.last_result}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200,200,255), 2)

    FRAME_WINDOW.image(frame, channels="BGR")

    # cooldown
    if st.session_state.cooldown > 0:
        st.session_state.cooldown -= 1

cap.release()
