import sys 
import math
import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
from mpl_toolkits.mplot3d import Axes3D

# ----- CONFIG -----
PORT = '/dev/cu.usbmodem1101'
BAUD = 115200
WINDOW = 200

ser = serial.Serial(PORT, BAUD, timeout=1)
pitch_buf = deque(maxlen=WINDOW)
roll_buf  = deque(maxlen=WINDOW)
x_idx     = deque(maxlen=WINDOW)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-90, 90)
ax.set_ylim(-90, 90)
ax.set_zlim(-1, 1)
ax.set_xlabel("Roll (X)")
ax.set_ylabel("Pitch (Y)")
ax.set_zlabel("Z")
ax.set_title("3D Pitch & Roll")

point, = ax.plot([], [], [], 'o', markersize=8)

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
    point.set_data([], [])
    point.set_3d_properties([])
    return point,

def update(frame):
    raw = ser.readline().decode(errors='ignore')
    if not raw:
        return point,
    pitch, roll = parse_line(raw)
    if pitch is None:
        return point,
    point.set_data([roll], [pitch])
    point.set_3d_properties([0])
    return point,

ani = FuncAnimation(fig, update, init_func=init, interval=30, blit=True)
plt.show()
