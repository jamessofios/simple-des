#!/usr/bin/env python3
#possible gui frontend
#looking into TKinter
from simpledes import *
from tkinter import *
"""
download python3-tk on debian to use tkinter
for python3 on debian 10(Stable)
"""

#tkinter's main window
top = Tk()
top.title("simpledes")
###########################################
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

#two labels for the result text to populate
l3 = Label(top, text = "Result:")
l3.grid(column = 0, row = 2)
#The result will be printed in a label to prevent the user
#from deleting the reult by accident
#l4 = Label(top, text = " ")
#l4.grid(column = 1, row = 2)

#Variabe for the radio buttons to work with
btn1 = IntVar()
#Encrypt and decrypt radio buttons
r1 = Radiobutton(top, text="Encrypt", variable = btn1, value = 1)
r1.grid(column=1,row=3)

r2 = Radiobutton(top, text="Decrypt", variable = btn1, value = 2)
r2.grid(column=1,row=4)

def onClick():

	#set variables from getting userdata
	#if encrypting
	if(btn1.get() == 1):
		bitstring = e1.get()
		key = e2.get()
		if(len(bitstring) != 8):
			print("Bitstring must have a length of 8")
		elif(len(key) != 10):
			print("Key must have a length of 10")
		else:
			cyphertext = encrypt(bitstring, key)
			Label(top, text=cyphertext).grid(column = 1, row = 2)
	#if decrypting
	elif(btn1.get() == 2):
		cyphertext = e1.get()
		key = e2.get()
		if(len(cyphertext) != 8):
			print("Bitstring must have a length of 8")
		elif(len(key) != 10):
			print("Key must have a length of 10")
		else:
			bitstring = decrypt(cyphertext, key)
			Label(top, text=bitstring).grid(column = 1, row = 2)
	else:
		print("Radio button error!")

#"The Go Button"
b1 = Button(top, text = "Go", command=onClick)
b1.grid(column=1,row=5)


###########################################
#tkinter's mainloop
top.mainloop()

