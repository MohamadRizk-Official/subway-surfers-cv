![Python](https://img.shields.io/badge/python-3.8+-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-orange)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Pose-green)
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

**Prerequisites**
```bash
pip install opencv-python mediapipe pyautogui
```

**Run**
```bash
python subway_controller.py
```

Then open Subway Surfers (browser or emulator), click into the game window, and start moving.

Press `Q` to quit.

---

## Tunable settings

These values are at the top of the file and control how the system feels:

| Setting | Default | What it does |
|---|---|---|
| `HAND_UP_RATIO` | `0.18` | How high your wrist must go above your shoulder to register |
| `SQUAT_RATIO` | `0.25` | How high the knee must rise above the hip to trigger a roll |
| `COOLDOWN_MS` | `280` | Minimum time between the same action firing twice |
| `MIRROR_VIEW` | `True` | Flips the webcam so movement feels natural |
| `SWAP_LR` | `True` | Corrects left/right orientation for mirrored view |
| `SHOW_DEBUG` | `True` | Shows pose skeleton and action labels on screen |

Thresholds scale automatically with shoulder width, so the system adapts to your body size and distance from the camera without manual recalibration.

---

## Key design decisions

**Pose over hand tracking** — Using `mp.solutions.pose` instead of `mp.solutions.hands` captures full-body gestures including squat detection, which hand-only tracking cannot do.

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
