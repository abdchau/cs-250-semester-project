import tkinter
import os
import tkinter.filedialog
from indexing import index
from config import *
from indexing.lexicon import load
from searching import search as srch
from indexing.lexicon import wordID_



lexicon, wordID_[0] = load(DICT_PATH)

def onClose():
	with open(os.path.join(DICT_PATH, 'metadata.json'), 'w', encoding="utf8") as f:
		json.dump(metadata, f, indent=2)

def addFile():
	file = tkinter.filedialog.askopenfilename()
	print(file)

	if file is not '':
		index.addFile(DICT_PATH, file, lexicon, BARREL_LENGTH)

def indexDataset():
	index.indexDataset(lexicon)	

def search(query):
	print(query)
	srch.searchquery(DICT_PATH,BARREL_LENGTH,query)
	pass