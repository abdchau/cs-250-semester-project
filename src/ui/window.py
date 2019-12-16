import tkinter
import tkinter.filedialog
import json
from ui.helper import *

def main():
	window = tkinter.Tk()
	window.title("Search Engine")

	label1 = tkinter.Label(window, text="Enter query:")

	txt = tkinter.Entry(window,width=15)
	btn1 = tkinter.Button(window, text="Index whole dataset", bg="green", fg="white", command=indexDataset)
	btn2 = tkinter.Button(window, text="Add file to index", bg="green", fg="white", command=addFile)
	searchBtn = tkinter.Button(window, text="Search", bg="green", fg="white", command=lambda :search(txt.get()))

	label1.grid(column=0,row=0)
	# label2.grid(column=0,row=2)
	btn1.grid(column=2)
	btn2.grid(column=2)
	searchBtn.grid(column=3, row=0)
	txt.grid(column=2, row=0)

	# window.filename = "hei"

	window.geometry('340x222')
	window.mainloop()
