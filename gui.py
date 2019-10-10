#!/usr/bin/env python3
#possible gui frontend
#looking into TKinter
from simpledes import *

"""
download python3-tk on debian to use tkinter
for python3 on debian 10(Stable)
"""
from tkinter import *

top = Tk()
top.title("simpledes")
# Code to add widgets will go here...

#label and entry box for the 8 bit bitstring
l1 = Label(top, text="Bitstring:")
l1.grid(column=0,row=0)

e1 = Entry(top, bd = 5)
e1.grid(column=1,row=0)

#label and entrybox for the 10 bit key bitstring
l2 = Label(top, text= "Key:")
l2.grid(column = 0, row = 1)

e2 = Entry(top, bd = 5)
e2.grid(column = 1, row = 1)

l3 = Label(top, text = "Result:")
l3.grid(column = 0, row = 2)

t1 = Label(top, text = " ")
t1.grid(column = 1, row = 2)

rbVar = IntVar()

r1 = Radiobutton(top, text="Encrypt", variable = rbVar, value = 1)
r1.grid(column=1,row=3)

r2 = Radiobutton(top, text="Decrypt", variable = rbVar, value = 2)
r2.grid(column=1,row=4)

b1 = Button(top, text = "Go")
b1.grid(column=1,row=5)

top.mainloop()
