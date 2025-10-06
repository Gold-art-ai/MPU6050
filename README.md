# MPU6050 Orientation Visualization Project

## Overview
This project demonstrates real-time orientation tracking using the MPU6050 sensor connected to an Arduino.  
It captures **pitch, roll, and yaw** data and visualizes it in multiple ways using Python.  
The goal is to understand motion, orientation, and real-time data visualization in 2D and 3D.

---

## Hardware Setup
- **Arduino board** (Uno, Nano, etc.)  
- **MPU6050 gyroscope + accelerometer sensor**  
- **Wiring**:
  - VCC → 5V  
  - GND → GND  
  - SDA → A4 (Arduino Uno/Nano)  
  - SCL → A5 (Arduino Uno/Nano)

---

## Software & Scripts
- `MPU6050.ino` – Arduino sketch to read orientation data and send via serial  
- `2d pitch.py` – 2D plot of pitch only, with a seesaw animation  
- `2d p&r.py` – 2D plot of pitch and roll  
- `3d p&r.py` – 3D point showing pitch & roll  
- `3d full.py` – Full 3D cube rotating with pitch, roll, yaw

**Dependencies**:  
```bash
pip install pyserial matplotlib numpy
