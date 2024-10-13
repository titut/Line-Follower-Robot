# Import Module
from tkinter import *

# create root window
root = Tk()

# root window title and dimension
root.title("Foodtruck Speed Controller")
# Set geometry (widthxheight)
root.geometry('800x450')

# adding a label to the root window
lbl = Label(root, text = "Current Speed: 50")
lbl.grid()

# adding Entry Field
txt = Entry(root, width=10)
txt.grid(column =1, row=1)

def clicked():
    res = "Current Speed: " + txt.get()
    lbl.configure(text = res)

# button widget with red color text
# inside
btn = Button(root, text = "Click me" ,
             fg = "red", command=clicked)
# set Button grid
btn.grid(column=2, row=1)

# all widgets will be here
# Execute Tkinter
root.mainloop()