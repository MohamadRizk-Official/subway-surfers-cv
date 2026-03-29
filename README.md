![Python](https://img.shields.io/badge/python-3.11-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-orange)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.14-green)
![Status](https://img.shields.io/badge/status-working-brightgreen)

# Subway Surfers — Body Gesture Controller

Play Subway Surfers with your body instead of the keyboard. A real-time computer vision system that tracks your pose through a webcam and converts physical movements into game controls.

> **Demo:** [Watch it in action on LinkedIn](https://www.linkedin.com/posts/mrizk36_python-computervision-opencv-ugcPost-7378892501946064896-kZwp)

---

## How it works

Your webcam feeds live frames into MediaPipe Pose, which tracks body landmarks in real time. The system reads your wrist and shoulder positions, detects gestures, and fires the corresponding keyboard input via PyAutoGUI — all with cooldown and edge-trigger logic so controls feel responsive, not spammy.

```
Webcam → OpenCV frames → MediaPipe landmarks → gesture logic → PyAutoGUI keypress → game
```

---

## Controls

| Gesture | Action |
|---|---|
| Raise left hand | Move left |
| Raise right hand | Move right |
| Raise both hands | Jump |
| Knee above hip | Roll |

Both-hands-up takes priority over single-hand detection, so jumps never misfire as lane switches.

---

## Technologies

- **Python** — core logic and game loop
- **OpenCV** — webcam capture and debug overlay rendering
- **MediaPipe Pose** — real-time body landmark tracking
- **PyAutoGUI** — keyboard input injection into the game

---

## Setup

> **Python version:** Use Python 3.11. Python 3.12 and above will cause NumPy and MediaPipe compatibility errors. Download Python 3.11 from [python.org](https://www.python.org/downloads/release/python-3119/) and check "Add Python to PATH" during install.

**Install dependencies**
```bash
py -3.11 -m pip install opencv-python mediapipe==0.10.14 pyautogui
```

**Run**
```bash
py -3.11 subway_controller.py
```

Then open Subway Surfers in your browser — [play it free on Poki](https://poki.com/en/g/subway-surfers).

> **Important:** Once the webcam window opens, click into the Subway Surfers game window so it has keyboard focus — otherwise your gestures will send keypresses to the wrong place and nothing will happen in game.

Press `Q` in the webcam window to quit.

---

## Tunable settings

These values are at the top of the file and control how the system feels:

| Setting | Default | What it does |
|---|---|---|
| `HAND_UP_RATIO` | `0.18` | How high your wrist must go above your shoulder to register |
| `KNEE_UP_RATIO` | `0.25` | How high the knee must rise above the hip to trigger a roll |
| `COOLDOWN_MS` | `280` | Minimum time between the same action firing twice |
| `MIRROR_VIEW` | `True` | Flips the webcam so movement feels natural |
| `SWAP_LR` | `True` | Corrects left/right orientation for mirrored view |
| `SHOW_DEBUG` | `True` | Shows pose skeleton and action labels on screen |

Thresholds scale automatically with shoulder width, so the system adapts to your body size and distance from the camera without manual recalibration.

---

## Key design decisions

**Pose over hand tracking** — Using `mp.solutions.pose` instead of `mp.solutions.hands` captures full-body gestures including knee detection, which hand-only tracking cannot do.

**Shoulder-width scaling** — All thresholds are calculated relative to the distance between your shoulders (`shw`), so the controller works at any distance from the camera.

**Edge triggers** — Actions only fire when a gesture *starts*, not while it's held. This prevents the game from receiving repeated inputs from a single pose.

**Cooldown system** — Each action has an independent timer, so a jump can't re-trigger for 280ms, keeping controls clean even with fast movement.

---

## Project structure

```
subway-surfers-cv/
│
├── subway_controller.py   # main controller script
└── README.md
```

---

## Disclaimer

This project is for educational and portfolio purposes. It does not modify or distribute any game assets.
