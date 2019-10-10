#!/usr/bin/env python3
#possible gui frontend
#looking into TKinter
from simpledes import *

#download python3-tk on debian to use
from tkinter import *

top = Tk()
# Code to add widgets will go here...

#label and entry box for the 8 bit bitstring
l1 = Label(top, text="Bitstring:")
l1.grid(column=0,row=0)

e1 = Entry(top, bd = 5)
e1.grid(column=1,row=0)

#label and entrybox for the 10 bit key bitstring
l2 = Label(top, text="Key:")
l2.grid(column=0,row=1)

e2 = Entry(top, bd =5)
e2.grid(column=1,row=1)

top.mainloop()
