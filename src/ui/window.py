import tkinter
import tkinter.filedialog
import json
from searching import search as srch
from indexing.index import Indexer
from config import *
from datetime import datetime
from ui.helper import Table


class Window(tkinter.Tk):

	def __init__(self):
		super(Window, self).__init__()
		self.title("Search Engine")
		self.indexer = Indexer()

		label1 = tkinter.Label(self, text="Enter query:")
		txt = tkinter.Entry(self,width=30)
		self.table = Table(self.indexer.metadata)

		indexButton = tkinter.Button(self, text="Index whole dataset",bg="green",
			fg="white", command=self.indexer.indexDataset)
		addButton = tkinter.Button(self, text="Add file to index", bg="green", fg="white", command=self.addFile)
		searchBtn = tkinter.Button(self, text="Search", bg="blue", fg="white",
			command=lambda: self.search(txt.get(), self.indexer.lexicon.lexDict,self.indexer.metadata))
		clearBtn = tkinter.Button(self, text="Clear results", bg='red', fg='white', command=self.table.clear)

		label1.place(x=10, y=45, in_=self)
		searchBtn.place(x=270, y=43, in_=self)
		txt.place(x=80, y=47, in_=self)

		indexButton.place(x=10, y=10, in_=self)
		addButton.place(x=150, y=10, in_=self)
		clearBtn.place(x=523, y=70, in_=self)

		self.table.place(x=7, y=100)

		txt.bind("<Return>", lambda e: self.search(txt.get(), self.indexer.lexicon.lexDict,self.indexer.metadata))
		self.protocol("WM_DELETE_WINDOW", self.onClose)
		self.geometry('630x350')


	def onClose(self):
		print(datetime.now(), 'Exiting program. Dumping lexicon, metadata and indexed documents.')
		
		# dump lexicon
		self.indexer.lexicon.dump()
		
		with open(os.path.join(DICT_PATH, 'metadata.json'), 'w', encoding="utf8") as f:
			json.dump(self.indexer.metadata, f, indent=2)

		with open(os.path.join(DICT_PATH, 'indexed_docs.json'), 'w', encoding="utf8") as docs:
			json.dump(self.indexer.indexedDocs, docs, indent=2)		
		self.destroy()


	def addFile(self):
		file = tkinter.filedialog.askopenfilename()
		print(file)

		if file is not '':
			self.indexer.addFile(DICT_PATH, file)

	def search(self,query,lexicon,metadata):
		print(datetime.now(), "Starting search.")
		results = self.arrangeResults(srch.searchQuery(DICT_PATH,query,lexicon,metadata))
		self.table.buildTree(results)
		print(datetime.now(), "Completed search.")


	def arrangeResults(self, results):
		lst = []
		try:
			for result in results:
				lst.append((result,)+tuple(self.indexer.metadata[result][:3])+(results[result],))
		except:
			tkinter.messagebox.showerror("Error", "No results found")
			print(datetime.now(), "No results found.")

		return lst