import tkinter
import tkinter.filedialog
from indexing import index
from config import *
from indexing.lexicon import load

lexicon, wordID = load(DICT_PATH)

def addFile():
	file = tkinter.filedialog.askopenfilename()
	print(file)

	if file is not '':
		index.addFile(DICT_PATH, file, lexicon, BARREL_LENGTH)

def indexDataset():
	index.indexDataset(lexicon)

def search(query):
	# do something
	print(query)
	pass