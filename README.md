# Virtual Air Calculator ✨

An innovative computer vision-powered application that allows users to perform calculations by pressing "virtual buttons" in the air using hand gestures.

## 📋 Project Overview

The Virtual Air Calculator replaces traditional physical calculators and touchscreen interfaces with a gesture-based system. Using just a webcam, the application tracks finger movements and detects when a user points to specific regions on the screen that correspond to calculator buttons. This project demonstrates the combination of computer vision, hand tracking, and gesture-based interfaces, representing a step toward more natural human-computer interaction.

<!-- ## 🎥 Demo

![Virtual Air Calculator Demo](demo.gif) -->

## ✨ Key Features

- **Real-time finger tracking** using MediaPipe Hands
- **Virtual calculator interface** with clearly visible keys (digits, operators, equals)
- **Air gesture input** - users press numbers/operators by pointing to regions on the screen
- **Dual input methods** - pinch gesture or dwell time for button presses
- **Debounce system** to avoid multiple unintended presses
- **Safe expression evaluation** with AST-based sanitization
- **Real-time visual feedback** with highlighted keys and expression display
- **Streamlit-based web interface** for easy accessibility

## 🏗️ Tech Stack

- **Python 3.8+** - Core programming language
- **OpenCV** - Real-time video processing and rendering
- **MediaPipe** - Hand and finger landmark detection
- **Streamlit** - Web-based frontend UI framework
- **NumPy** - Array operations and mathematical computations
- **AST Module** - Safe expression parsing and evaluation
- **Python Standard Library** - Various utilities and helpers

## 📁 Project Structure

```
virtual-air-calculator/
│
├── main.py                 # Main OpenCV application (standalone version)
├── streamlit_app.py        # Streamlit web application
├── calc_engine.py          # Safe expression evaluation logic
├── keypad.py               # Keypad layout and geometry utilities
├── utils.py                # Helper functions (drawing, math, etc.)
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── .gitignore             # Git ignore rules
```

## 🔧 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Krintox/Virtual_Calculator
   cd virtual-air-calculator
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 How to Run

### Option 1: Standalone OpenCV Application
```bash
python main.py
```

### Option 2: Streamlit Web Application
```bash
streamlit run streamlit_app.py
```

The application will open your webcam and display the virtual calculator interface.

## 🎮 How to Use

1. Position yourself so your hand is visible to the webcam
2. The virtual calculator keypad appears on the right side of the screen
3. Use your index finger to point to buttons:
   - **Pinch method**: Bring your thumb and index finger together while pointing at a button
   - **Dwell method**: Hover over a button for a moment (approximately 1 second)
4. View your expression and results at the top of the screen
5. Press 'C' to clear or '=' to evaluate your expression

## ⚙️ Configuration Options

The application includes several configurable parameters in the code:

- `PINCH_THRESHOLD_RATIO`: Sensitivity of pinch detection
- `DWELL_FRAMES`: Number of frames required for dwell-based activation
- `COOLDOWN_FRAMES`: Cooldown period between button presses
- Keypad dimensions and positioning
- Visual styling of buttons and interface

## 🔐 Security Features

The calculator includes a secure expression evaluator that:

- Parses expressions using Python's AST module
- Only allows approved mathematical operations
- Blocks function calls, imports, and other potentially dangerous operations
- Prevents code injection attacks

## 🧠 How It Works

### 1. Hand Detection
- MediaPipe Hands processes the webcam feed to detect hand landmarks
- Tracks 21 key points on each detected hand
- Focuses on the index finger tip (landmark 8) and thumb tip (landmark 4)

### 2. Gesture Recognition
- **Pointing detection**: Determines which calculator button the user is pointing at
- **Pinch detection**: Measures distance between index finger and thumb tips
- **Dwell detection**: Tracks how long a user hovers over a button

### 3. Input Processing
- When a gesture is detected, the corresponding button press is registered
- Expressions are built sequentially
- The safe evaluator processes mathematical expressions

### 4. Interface Rendering
- OpenCV draws the calculator interface overlay
- Visual feedback shows highlighted and pressed buttons
- Current expression and results are displayed in real-time


---

**Note**: This application requires a webcam and works best in well-lit environments with a clean background. For optimal performance, ensure your hands are clearly visible to the camera and avoid wearing accessories that might interfere with hand tracking.