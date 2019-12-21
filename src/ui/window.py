import tkinter
import tkinter.filedialog
import json
from searching import search as srch
from indexing.index import Indexer
from config import *
from datetime import datetime
from searching import search as srch

class Window(tkinter.Tk):

	def __init__(self):
		super(Window, self).__init__()
		self.title("Search Engine")
		self.indexer = Indexer()

		label1 = tkinter.Label(self, text="Enter query:")
		txt = tkinter.Entry(self,width=15)

		indexButton = tkinter.Button(self, text="Index whole dataset",bg="green",
			fg="white", command=self.indexer.indexDataset)
		addButton = tkinter.Button(self, text="Add file to index", bg="green", fg="white", command=self.addFile)
		searchBtn = tkinter.Button(self, text="Search", bg="green", fg="white", command=lambda:self.search(txt.get()))

		label1.grid(column=0,row=0)
		indexButton.grid(column=2)
		addButton.grid(column=2)
		searchBtn.grid(column=3, row=0)
		txt.grid(column=2, row=0)

		self.protocol("WM_DELETE_WINDOW", self.onClose)
		self.geometry('340x222')


	def onClose(self):
		print(datetime.now(), 'Exiting program. Dumping lexicon, metadata and indexed documents.')
		
		# dump lexicon
		self.indexer.lexicon.dump()
		
		with open(os.path.join(DICT_PATH, 'metadata.json'), 'w', encoding="utf8") as f:
			json.dump(self.indexer.metadata, f, indent=2)

		with open(os.path.join(DICT_PATH, 'indexed_docs.json'), 'w', encoding="utf8") as docs:
			json.dump(indexedDocs, docs, indent=2)		
		self.destroy()


	def addFile(self):
		file = tkinter.filedialog.askopenfilename()
		print(file)

		if file is not '':
			self.indexer.addFile(DICT_PATH, file)

	def search(self,query):
		print(query)
		srch.searchquery(DICT_PATH,query)		