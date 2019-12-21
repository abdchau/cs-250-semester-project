import tkinter
import os
import tkinter.filedialog
from indexing.index import Indexer
from config import *
from searching import search as srch

indexer = Indexer()

def onClose(window):
	with open(os.path.join(DICT_PATH, 'metadata.json'), 'w', encoding="utf8") as f:
		json.dump(metadata, f, indent=2)

	with open(os.path.join(DICT_PATH, 'indexed_docs.json'), 'w', encoding="utf8") as docs:
		json.dump(indexedDocs, docs, indent=2)	
	window.destroy()

def addFile():
	file = tkinter.filedialog.askopenfilename()
	print(file)

	if file is not '':
		indexer.addFile(DICT_PATH, file, BARREL_LENGTH)

def indexDataset():
	indexer.indexDataset()

def search(query):
	print(query)
	srch.searchquery(DICT_PATH,BARREL_LENGTH,query)
