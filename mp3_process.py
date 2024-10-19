"""
Receive wheel velocity data from Arduino serially and plot.
"""

import matplotlib.pyplot as plt
import serial
import pandas as pd

# serial constants
PORT = "COM4"
BAUDRATE = 9600
serialPort = serial.Serial(PORT, BAUDRATE, timeout=1)

# useful variables
millis = 0.010 # 50 millis per serial line
times = [0.0 - millis] # start with setback to line up time properly
left_vels = []
right_vels = []
ir_vals = [[], [], [], []]

# receive data from Arduino
while times[-1] < 30.0:
    lineOfData = serialPort.readline().decode()
    # there is data
    if len(lineOfData) > 0:
        # split data
        data = lineOfData.split(",")
        data[5] = data[5][:-2]
        [left_vel, right_vel, ir1, ir2, ir3, ir4] = [int(x) for x in data]
        ir_list = [ir1, ir2, ir3, ir4]

        print(ir_list)

        # append velocities
        left_vels.append(left_vel)
        right_vels.append(right_vel)

        # append IR values
        for i, ir_val in enumerate(ir_list):
            ir_vals[i].append(ir_val)

        # calculate time
        times.append(times[-1] + millis) # 50 millis per scan
    else:
        print(f"No line found. Current point count: {len(times)}")

# first, remove starter time value
del times[0]

d = {
    "wheel_left": left_vels,
    "wheel_right": right_vels,
    "ir_0": ir_vals[0],
    "ir_1": ir_vals[1],
    "ir_2": ir_vals[2],
    "ir_3": ir_vals[3]
}

df=pd.DataFrame(data=d)
df.to_csv("data.csv")

"""
# now start plotting
fig, ax1 = plt.subplots()
fig.tight_layout()
ax2 = ax1.twinx()
ax1.set_xlabel('time (s)')

# plot wheel velocities
ax1.set_ylabel('wheel velocity (m/s)', color='tab:blue')
ax1.plot(times, left_vels, color=(0, 0, 1)) # left wheel
ax1.plot(times, right_vels, color=(0, 1, 1)) # right wheel
ax1.tick_params(axis='y', labelcolor='tab:blue')
plt.show()
# plot analog values
ax2.set_ylabel('IR analog values', color='tab:red')
plt.plot(times, ir_vals[0], c=[255, 0, 0]) # A0
plt.plot(times, ir_vals[1], c=[255, 100, 0]) # A1
plt.plot(times, ir_vals[2], c=[255, 200, 0]) # A2
plt.plot(times, ir_vals[3], c=[255, 255, 0]) # A3
ax2.tick_params(axis='y', labelcolor='tab:red')

# label and show
plt.legend(["Left wheel", "Right wheel", "A0", "A1", "A2", "A3"])
plt.show()
"""