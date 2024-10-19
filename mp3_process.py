"""
Receive wheel velocity data from Arduino serially and plot.
"""
import matplotlib
import matplotlib.pyplot as plt
import serial
import pandas as pd

# serial constants
PORT = "COM4"
BAUDRATE = 9600
LIVE = False

# useful variables
millis = 0.010 # 10 millis per serial line
times = []

if LIVE == True:
    serialPort = serial.Serial(PORT, BAUDRATE, timeout=1)
    # set up space for variables
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
        else:
            print(f"No line found. Current point count: {len(left_vels)}")

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
else:
    data = pd.read_csv("data.csv")

    # make times
    for index, row in data.iterrows():
        times.append(millis * index)

    # now start plotting
    fig, ax1 = plt.subplots()
    fig.tight_layout()
    ax2 = ax1.twinx()
    ax1.set_xlabel('time (s)')

    # plot wheel velocities
    print("Working on wheel velocities...")
    ax1.set_ylabel('wheel velocity (m/s)', color='tab:blue')
    ax1.plot(times, data["wheel_left"].values, color="blue") # left wheel
    ax1.plot(times, data["wheel_right"].values, color="cyan") # right wheel
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # plot analog values
    print("Working on IR Values...")
    ax2.set_ylabel('IR analog values', color='tab:red')
    ax2.plot(times, data["ir_0"].values, c="magenta") # A0
    ax2.plot(times, data["ir_1"].values, c="red") # A1
    ax2.plot(times, data["ir_2"].values, c="orange") # A2
    ax2.plot(times, data["ir_3"].values, c="yellow") # A3
    ax2.tick_params(axis='y', labelcolor='tab:red')

    # label and show
    ax1.legend(data.columns[1:3], loc="upper left")
    ax2.legend(data.columns[3:], loc="upper right")
    plt.show()

print("Done")