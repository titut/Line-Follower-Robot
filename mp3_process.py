"""
Receive wheel velocity data from Arduino serially and plot.
"""

import matplotlib.pyplot as plt
import serial

# serial constants
PORT = "COM6"
BAUDRATE = 9600
serialPort = serial.Serial(PORT, BAUDRATE, timeout=1)

# lists
TOTAL_PTS = 100
times = []
left_vels = []
right_vels = []

# receive data from Arduino
while float(times[-1]) < 20.0:
    lineOfData = serialPort.readline().decode()
    # there is data
    if len(lineOfData) > 0:
        time, left_vel, right_vel = lineOfData.split(",")
        times.append(time)
        left_vels.append(left_vel)
        right_vels.append(right_vel)
    else:
        print(f"No line found. Current point count: {len(times)}")


# plot points
plt.scatter(times, left_vels, c=100)
plt.scatter(times, right_vels, c=50)
plt.xlabel("Time (seconds)")
plt.ylabel("Wheel velocity (m/s)")
plt.legend(["Left wheel", "Right wheel"])
plt.show()
