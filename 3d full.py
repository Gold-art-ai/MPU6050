import sys 
import math
import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

PORT = 'COM3'  # <- change if needed
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=1)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim([-1,1])
ax.set_ylim([-1,1])
ax.set_zlim([-1,1])
ax.set_xlabel("X (Roll)")
ax.set_ylabel("Y (Pitch)")
ax.set_zlabel("Z (Yaw)")
ax.set_title("Full 3D Orientation: Pitch, Roll, Yaw")

# Define a unit cube centered at origin
r = [-0.5, 0.5]
vertices = np.array([[x,y,z] for x in r for y in r for z in r])
faces = [
    [0,1,3,2], [4,5,7,6], [0,1,5,4],
    [2,3,7,6], [0,2,6,4], [1,3,7,5]
]
cube = Poly3DCollection([], facecolors='cyan', linewidths=1, edgecolors='r', alpha=0.25)
ax.add_collection3d(cube)

def rotation_matrix(roll, pitch, yaw):
    r, p, y = np.radians([roll, pitch, yaw])
    Rx = np.array([[1,0,0],[0,np.cos(r),-np.sin(r)],[0,np.sin(r),np.cos(r)]])
    Ry = np.array([[np.cos(p),0,np.sin(p)],[0,1,0],[-np.sin(p),0,np.cos(p)]])
    Rz = np.array([[np.cos(y),-np.sin(y),0],[np.sin(y),np.cos(y),0],[0,0,1]])
    return Rz @ Ry @ Rx

def parse_line(line):
    try:
        parts = line.strip().split(',')
        if len(parts) < 3:
            return None, None, None
        pitch = float(parts[0])
        roll  = float(parts[1])
        yaw   = float(parts[2])
        return pitch, roll, yaw
    except:
        return None, None, None

def update(frame):
    raw = ser.readline().decode(errors='ignore')
    if not raw:
        return cube,
    pitch, roll, yaw = parse_line(raw)
    if pitch is None:
        return cube,

    R = rotation_matrix(roll, pitch, yaw)
    transformed = np.dot(vertices, R.T)
    cube.set_verts([transformed[face] for face in faces])
    return cube,

ani = FuncAnimation(fig, update, interval=30, blit=True)
plt.show()
