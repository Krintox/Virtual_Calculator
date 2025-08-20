# utils.py
import math
import cv2
from keypad import Key
from typing import Tuple, List

def point_in_rect(px: int, py: int, key: Key) -> bool:
    return key.x1 <= px <= key.x2 and key.y1 <= py <= key.y2

def dist(a: Tuple[int,int], b: Tuple[int,int]) -> float:
    return math.hypot(a[0]-b[0], a[1]-b[1])

def draw_keys(img, keys: List[Key], highlight: Key = None, pressed: Key = None):
    for k in keys:
        color = (200, 200, 200)
        thickness = 2
        if pressed is not None and k.label == pressed.label:
            # filled highlight for pressed
            cv2.rectangle(img, (k.x1, k.y1), (k.x2, k.y2), (0, 180, 0), -1)
            text_color = (255,255,255)
            thickness = 2
        elif highlight is not None and k.label == highlight.label:
            cv2.rectangle(img, (k.x1, k.y1), (k.x2, k.y2), (0, 120, 255), 3)
            text_color = (255,255,255)
        else:
            cv2.rectangle(img, (k.x1, k.y1), (k.x2, k.y2), (180, 180, 180), thickness)
            text_color = (0,0,0)

        # center text
        font = cv2.FONT_HERSHEY_SIMPLEX
        (text_w, text_h), _ = cv2.getTextSize(k.label, font, 1.0, 2)
        cx = k.x1 + (k.x2 - k.x1) // 2 - text_w // 2
        cy = k.y1 + (k.y2 - k.y1) // 2 + text_h // 2
        cv2.putText(img, k.label, (cx, cy), font, 1.0, text_color, 2, cv2.LINE_AA)
