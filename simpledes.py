#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Edge cases:

    This program checks to see if the 8bit plain text and the 10bit key are the correct lengths, but it does not check to make sure that the user only inputs 1's and 0's.  This can become a problem because the program with throw an error message if the user inputs anything but 1's and 0's.  The user input is casted as a string to avoid the 1's and 0's being interpreted as integers rather than bit strings.
'''
import sys
from tkinter import *
from tkinter import messagebox
from re import *

#predefined permutations
ip = (2, 6, 3, 1, 4, 8, 5, 7)
ip_inverse = (4, 1, 3, 5, 7, 2, 8, 6)
ep = (4, 1, 2, 3, 2, 3, 4, 1)
p10 = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
p8 = (6, 3, 7, 4, 8, 5, 10, 9)
p4 = (2, 4, 3, 1)

#predefined sboxes
sb0 = ((1, 0, 3, 2),
      (3, 2, 1, 0),
      (0, 2, 1, 3),
      (3, 1, 3, 2))

sb1 = ((0, 1, 2, 3),
      (2, 0, 1, 3),
      (3, 0, 1, 0),
      (2, 1, 0, 3))

#permute takes a bitstring and a predefined permutation as input and outputs a new permuted bitstring
def permute(bitstring, permutation):
    new = ''
    for i in permutation:
        new += bitstring[i - 1]
    return new

#left_half takes a bitstring as input and breaks it in half, returning the left side
def left_half(bitstring):
    return bitstring[:int(len(bitstring)/2)]

#right_half takes a bitstring as input and breaks it in half, returning the right side
def right_half(bitstring):
    return bitstring[int(len(bitstring)/2):]

#lshift takes a bitstring as input and shifts the two halves of it to the left by one
def lshift(bitstring):
    shifted_left_half = left_half(bitstring)[1:] + left_half(bitstring)[0]
    shifted_right_half = right_half(bitstring)[1:] + right_half(bitstring)[0]
    return shifted_left_half + shifted_right_half

#key1 applys all of the functions necessary to generate k1 from the original 10 bit key
def key1(key):
    return permute(lshift(permute(key, p10)), p8)

#key2 applys all of the functions necessary to generate k2 from the original 10 bit key
def key2(key):
    return permute(lshift(lshift(lshift(permute(key, p10)))), p8)

#xor takes two bitstrings as input XOR-ing them and giving the result as output
def xor(bitstring, key):
    new = ''
    for str_bit, key_bit in zip(bitstring, key):
        new += str(((int(str_bit) + int(key_bit)) % 2))
    return new

#sblookup takes a bitstring and an sbox as input.
#using the bitstring value, it gets the corresponding value from the sbox.
#it then converts the values from the sbox to binary and returns that binary value
def sblookup(bitstring, sbox):
    row = int(bitstring[0] + bitstring[3], 2)
    col = int(bitstring[1] + bitstring[2], 2)
    return '{0:02b}'.format(sbox[row][col])

#applys the functions that make up f_K
def f_k(bitstring, key):

    #breaks the bitstring into right and left sides
    L = left_half(bitstring)
    R = right_half(bitstring)

    #expand and permute the right side of the 8 bit plaintext
    bitstring = permute(R, ep)

    #xor the previous output with the key
    bitstring = xor(bitstring, key)

    #looks up the left and right halves of the previous output in sbox0 and sbox1 respectively
    #then it recombines the sbox values into 'bitstring'
    bitstring = sblookup(left_half(bitstring), sb0) + sblookup(right_half(bitstring), sb1)

    #appys p4 to 'bitstring'
    bitstring = permute(bitstring, p4)

    #returns the previous output xor'd with the left half of the original bitstring
    return xor(bitstring, L)

#applys the functions that make up the encryption process
def encrypt(plain_text,key):

    #permutes the plaintext using ip
    bitstring = permute(plain_text, ip)

    #holds the output of fk using the previous output and k1 and input
    temp = f_k(bitstring, key1(key))

    #combines the output of fk with the right half of the result of ip
    bitstring = right_half(bitstring) + temp

    #puts the previous output and k2 through the fk function
    bitstring = f_k(bitstring, key2(key))

    #ip inverse permutes the previous output combined with the output of fk(ip, k1)
    return (permute(bitstring + temp, ip_inverse))

#applys the functions that make up the decryption process
def decrypt(cipher_text,key):
    #permutes the cyphertext using ip
    bitstring = permute(cipher_text, ip)

    #holds the output of fk using the previous output and k2 and input
    temp = f_k(bitstring, key2(key))

    #combines the output of fk with the right half of the result of ip
    bitstring = right_half(bitstring) + temp

    #puts the previous output and k1 through the fk function
    bitstring = f_k(bitstring, key1(key))

    #ip inverse permutes the previous output combined with the output of fk(ip, k2)
    return (permute(bitstring + temp, ip_inverse))

def main():
	if(len(sys.argv) < 2):
		print("Welcome! Running in graphical mode.")
		print("Type (h)elp for help.")
		print("Example of (h)elp:")
		print(sys.argv[0] + " h")
		gui()
	elif(len(sys.argv) == 4):
		if(sys.argv[1] == "encrypt" or sys.argv[1] == "e"):
			plaintext = str(sys.argv[2])
			key = str(sys.argv[3])
			if(len(plaintext) == 8 and len(key) == 10):
				print(encrypt(plaintext,key))
			if(len(key) != 10):
				print("Error!")
				print("Key must me 10 bits.")
			if(len(plaintext) != 8):
				print("Error!")
				print("Plaintext must me 8 bits.")
		elif(sys.argv[1] == "decrypt" or sys.argv[1] == "d"):
			cyphertext = str(sys.argv[2])
			key = str(sys.argv[3])
			if(len(cyphertext) == 8 and len(key) == 10):
				print(decrypt(cyphertext,key))
			if(len(key) != 10):
				print("Error!")
				print("Key must me 10 bits.")
			if(len(cyphertext) != 8):
				print("Error!")
				print("Cyphertext must me 8 bits.")
	elif(len(sys.argv) == 2):
		if(sys.argv[1] == "help" or sys.argv[1] == "h"):
			print("Type (e)ncrypt or (d)ecrypt, 8 bits, and a 10 bit key to run this program.")
			print("Example of encrypt:")
			print(sys.argv[0] +  " e 11111111 1111111111")
			print("Example of decrypt:")
			print(sys.argv[0] + " d 11111111 1111111111")

def gui():
	"""
	download python3-tk on debian to use tkinter
	for python3 on debian 10(Stable)
	"""

	#tkinter's main window
	top = Tk()
	top.title("simpledes")
	#top.geometry("300x300")
	###########################################
	# Code to add widgets will go here...

	#label and entry box for the 8 bit bitstring
	l1 = Label(top, text="Bitstring(8 bits):")
	l1.grid(column=0,row=0)

	e1 = Entry(top, bd = 5)
	e1.grid(column=1,row=0)

	#label and entrybox for the 10 bit key bitstring
	l2 = Label(top, text= "Key(10 bits):")
	l2.grid(column = 0, row = 1)

	e2 = Entry(top, bd = 5)
	e2.grid(column = 1, row = 1)

	#two labels for the result text to populate
	l3 = Label(top, text = "Result(8 bits):")
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
	def isValid(bitstring, key):
		pattern = compile("^[01]+$")
		if( not pattern.match(bitstring) or not pattern.match(key) ):
			print("String format error!")
			messagebox.showerror("Error", "All fields must contain zeros or ones!")
		elif(len(bitstring) != 8):
			print("Bitstring must have a length of 8!")
			messagebox.showerror("Error", "Bitstring must have a length of 8!")
		elif(len(key) != 10):
			print("Key must have a length of 10!")
			messagebox.showerror("Error", "Key must have a length of 10!")
		else:
			return True
	def onClick():

		#set variables from getting userdata
		#if encrypting
		if(btn1.get() == 1):
			bitstring = e1.get()
			key = e2.get()

			if(isValid(bitstring, key)):
				cyphertext = encrypt(bitstring, key)
				Label(top, text=cyphertext).grid(column = 1, row = 2)
		#if decrypting
		elif(btn1.get() == 2):
			cyphertext = e1.get()
			key = e2.get()

			if(isValid(cyphertext, key)):
				bitstring = decrypt(cyphertext, key)
				Label(top, text=bitstring).grid(column = 1, row = 2)
		#
		else:
			print("Radio button error!")
			messagebox.showerror("Error", "At least one radio button must be selected!")

	#"The Go Button"
	b1 = Button(top, text = "Go", command=onClick)
	b1.grid(column=1,row=5)

	###########################################
	#tkinter's mainloop
	top.mainloop()

if __name__ == "__main__":
	main()
