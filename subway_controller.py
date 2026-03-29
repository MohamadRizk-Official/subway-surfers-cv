import time, math
import cv2
import mediapipe as mp
import pyautogui

# =========== TUNABLES ===============
MIRROR_VIEW      = True     # mirror the webcam view for natural control
HAND_UP_RATIO    = 0.18     # how far above the shoulder the wrist must be (fraction of shoulder width)
KNEE_UP_RATIO    = 0.25     # knee rises above hip -> roll
COOLDOWN_MS      = 280      # min time between same action
SWAP_LR          = True     # True => swap Left/Right outputs so "my left hand" moves left in game
SHOW_DEBUG       = True
# ============================

pyautogui.FAILSAFE = False

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    model_complexity=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)
draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Edge-trigger state + per-action cooldowns
prev = {"left_up": False, "right_up": False, "both_up": False, "knee_up": False}
last = {"left":0, "right":0, "up":0, "down":0}

def press(key):
    pyautogui.press(key)

def send_left():
    # If your game movement feels inverted, flip SWAP_LR above
    press('right') if SWAP_LR else press('left')

def send_right():
    press('left') if SWAP_LR else press('right')

while True:
    ok, frame = cap.read()
    if not ok:
        break
    if MIRROR_VIEW:
        frame = cv2.flip(frame, 1)

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = pose.process(rgb)

    actions = []
    now = time.time()*1000

    if res.pose_landmarks:
        lm = res.pose_landmarks.landmark

        # Landmarks we need
        l_sh, r_sh = lm[11], lm[12]
        l_w , r_w  = lm[15], lm[16]
        l_hip, r_hip = lm[23], lm[24]
        l_k  , r_k   = lm[25], lm[26]

        # Scale by shoulder width so thresholds auto-fit your size/distance
        shw = max(1e-6, abs(r_sh.x - l_sh.x))

        # --- HANDS-UP DETECTION (per hand) -----
        # y smaller = higher on image
        left_up  = l_w.y < (l_sh.y - HAND_UP_RATIO*shw)
        right_up = r_w.y < (r_sh.y - HAND_UP_RATIO*shw)
        both_up  = left_up and right_up

        # --- PRIORITY: JUMP when BOTH hands up -----
        if both_up and not prev["both_up"] and (now - last["up"] > COOLDOWN_MS):
            press('up'); last["up"] = now; actions.append("JUMP")

        # If not both, allow single-hand L/R (edge trigger + cooldown)
        elif left_up and not right_up and not prev["left_up"] and (now - last["left"] > COOLDOWN_MS):
            send_left(); last["left"] = now; actions.append("LEFT")

        elif right_up and not left_up and not prev["right_up"] and (now - last["right"] > COOLDOWN_MS):
            send_right(); last["right"] = now; actions.append("RIGHT")

        # ----- KNEE ABOVE HIP → ROLL -----
        thigh_len = max(1e-6, ((l_k.y + r_k.y)/2.0) - ((l_hip.y + r_hip.y)/2.0))
        knee_up = thigh_len < KNEE_UP_RATIO
        if knee_up and not prev["knee_up"] and (now - last["down"] > COOLDOWN_MS):
            press('down'); last["down"] = now; actions.append("ROLL")

        # Update edge states
        prev["left_up"]  = left_up
        prev["right_up"] = right_up
        prev["both_up"]  = both_up
        prev["knee_up"]  = knee_up

        # Debug overlay
        if SHOW_DEBUG:
            draw.draw_landmarks(frame, res.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            cv2.putText(frame, f"L_up={left_up}  R_up={right_up}  BOTH={both_up}", (10,30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
            cv2.putText(frame, f"thigh_len={thigh_len:.2f}  knee_up={knee_up}", (10,60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)
            if actions:
                cv2.putText(frame, " | ".join(actions), (10, 95),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0), 3)

    cv2.imshow("Subway Surfers — Hands Up Control (Q to quit)", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
