# Import Module
from tkinter import *
import serial

arduinoPort = "COM4"
baudRate = 9600
serialPort = serial.Serial(arduinoPort, baudRate, timeout=1)

# current speed variable
current_speed = 0

# create root window
root = Tk()

# configure column and rows
padding = 50
for i in range(3):
    root.columnconfigure(i, weight=1, minsize=padding)
    root.rowconfigure(i, weight=1)

# root window title and dimension
root.title("Foodtruck Speed Controller")
# Set geometry (widthxheight)
root.geometry('300x150')

# adding a label to the root window
lbl = Label(root, text = "Current Speed: " + str(current_speed), font=("Arial", 17))
lbl.grid(row=0, column=1)

def sendMessage(x):
    serialPort.write(bytes(str(x), 'utf-8'))
    print("SENT " + str(x))
    return 0

# adding a label to the root window
def change_speed_by_user_input():
    inp = user_input.get()
    if inp.isnumeric():
        current_speed = int(inp)
        lbl.config(text="Current Speed: " + str(current_speed))
        sendMessage(current_speed)
        user_input.delete(0, END)

user_input = Entry()
change_button = Button(text="Change", command=change_speed_by_user_input)
user_input.grid(row=1, column=1, sticky=W)
change_button.grid(row=1, column=1, sticky=E)

# adding a label to the root window
def increase_speed():
    global current_speed
    current_speed = current_speed + 2
    lbl.config(text="Current Speed: " + str(current_speed))
    sendMessage(current_speed)
    user_input.delete(0, END)

def decrease_speed():
    global current_speed
    current_speed = current_speed - 2
    lbl.config(text="Current Speed: " + str(current_speed))
    sendMessage(current_speed)
    user_input.delete(0, END)

decrease_button = Button(text="Decrease", command=decrease_speed)
increase_button = Button(text="Increase", command=increase_speed)
decrease_button.grid(row=2, column=1, sticky=W, padx=38)
increase_button.grid(row=2, column=1, sticky=E, padx=38)

root.mainloop()