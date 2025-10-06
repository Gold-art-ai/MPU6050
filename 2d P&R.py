import sys 
import math
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# ----- CONFIG -----
PORT = 'COM3'  # <- change if needed
BAUD = 115200
WINDOW = 200

ser = serial.Serial(PORT, BAUD, timeout=1)

pitch_buf = deque(maxlen=WINDOW)
roll_buf  = deque(maxlen=WINDOW)
x_idx     = deque(maxlen=WINDOW)

fig, ax = plt.subplots(figsize=(9,5))
(line_pitch,) = ax.plot([], [], label="Pitch (°)")
(line_roll,)  = ax.plot([], [], label="Roll (°)")

ax.set_xlim(0, WINDOW)
ax.set_ylim(-90, 90)
ax.set_xlabel("Samples")
ax.set_ylabel("Angle (°)")
ax.set_title("MPU6050 Pitch & Roll (2D)")
ax.legend()

def parse_line(line):
    try:
        parts = line.strip().split(',')
        if len(parts) < 2:
            return None, None
        pitch = float(parts[0])
        roll  = float(parts[1])
        return pitch, roll
    except:
        return None, None

def init():
    line_pitch.set_data([], [])
    line_roll.set_data([], [])
    return line_pitch, line_roll

def update(frame):
    for _ in range(5):
        raw = ser.readline().decode(errors='ignore')
        if not raw:
            break
        pitch, roll = parse_line(raw)
        if pitch is None:
            continue
        pitch_buf.append(pitch)
        roll_buf.append(roll)
        x_idx.append(len(x_idx) + 1 if x_idx else 1)

    xs = list(range(len(x_idx)))
    line_pitch.set_data(xs, list(pitch_buf))
    line_roll.set_data(xs, list(roll_buf))
    ax.set_xlim(max(0, len(xs)-WINDOW), max(WINDOW, len(xs)))
    return line_pitch, line_roll

ani = animation.FuncAnimation(fig, update, init_func=init, interval=30, blit=True)
plt.tight_layout()
plt.show()
