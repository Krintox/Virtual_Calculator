# keypad.py
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Key:
    label: str
    x1: int
    y1: int
    x2: int
    y2: int

def build_keys(frame_w: int, frame_h: int,
               cols: int = 4, rows: int = 4,
               width_ratio: float = 0.35,
               height_ratio: float = 0.7,
               margin: int = 20) -> List[Key]:
    """
    Build a 4x4 keypad positioned on the right side of the frame.
    Returns list of Key objects with pixel coordinates.
    """
    labels = [
        ["1", "2", "3", "+"],
        ["4", "5", "6", "-"],
        ["7", "8", "9", "*"],
        ["C", "0", "=", "/"]
    ]

    area_w = int(frame_w * width_ratio)
    area_h = int(frame_h * height_ratio)
    area_x = frame_w - area_w - margin
    area_y = int((frame_h - area_h) / 2)

    cell_w = area_w // cols
    cell_h = area_h // rows

    keys: List[Key] = []
    for r in range(rows):
        for c in range(cols):
            x1 = area_x + c * cell_w
            y1 = area_y + r * cell_h
            x2 = x1 + cell_w - 2
            y2 = y1 + cell_h - 2
            label = labels[r][c]
            keys.append(Key(label, x1, y1, x2, y2))

    return keys
