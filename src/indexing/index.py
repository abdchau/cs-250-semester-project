from tqdm import tqdm
import os
from indexing.helper import *
from indexing.lexicon import Lexicon
from indexing.forward import ForwardIndexer
from indexing.inverted import InvertedIndexer
from datetime import datetime
from config import *


class Indexer:
	"""docstring for Indexer"""
	def __init__(self):
		self.docID = 100000
		self.lexicon = Lexicon(DICT_PATH)

		self.barrelLength = BARREL_LENGTH
		self.indexedDocs = self.loadIndexedDocs()
		self.metadata = self.loadMetadata()

		print(self.docID)
		self.forwardIndexer = ForwardIndexer()
		self.invertedIndexer = InvertedIndexer()
		

	def addFile(self, dictDir, file):
		"""
		arguments:
			- dictDir: the path of the directory containing the
			dictionaries for the forward and the inverted index
			- file: the path to the file that is to be added
			- lexicon: the lexicon to be used for indexing
			- barrelLength: the range of words in a single barrel

		This function updates the lexicon to accommodate the
		new file and adds the file to the forward and inverted
		indexes.

		return: None
		"""

		# if document is already indexed, return
		if indexedDocs.get(file[-20:]) is not None:
			print("return")
			return
		print(indexedDocs)
		print(file)
		print("not return")

		author, title, tokens, url, published, lenText = readFile(file)

		smalltokens = clean(author+" "+title)
		tokens = clean(tokens)

		self.lexicon.wordID = self.lexicon.processFile(self.lexicon, self.lexicon.wordID, tokens)

		# get unique, sorted wordIDs present in the file
		wordIDs = sorted(set([self.lexicon.lexDict[token] for token in tokens]))

		# get all barrels that are to be updated
		barrels = sorted(set([self.lexicon.wordID//self.barrelLength for self.lexicon.wordID in wordIDs]))

		forwardBarrels = self.forwardIndexer.addFile(dictDir, 
			self.lexicon, tokens, self.docID, barrels, self.barrelLength)

		self.invertedIndexer.addFile(dictDir, wordIDs, self.docID, barrels, forwardBarrels)
		self.lexicon.dump()

		indexedDocs[file[-20:]] = self.docID

		# store document's metadata
		self.addMetadata(self.docID, author, title, url,published,lenText)
		print(self.docID)
		self.docID+=1
		# print(metadata)

	def indexDataset(self):
		"""
		arguments:
			- lexicon: the main lexicon that is to be held
			in memory

		This function will iterate over the dataset provided
		in DATASET_PATH and will index it. The indexes and
		lexicon will be written to the DICT_PATH directory.

		return: None
		"""
		print(self.docID)
		print(datetime.now(), "Generating lexicon and forward index")
		shortforwardBarrels = dict()
		forwardBarrels = dict()

		for file in tqdm(os.listdir(DATA_PATH)):
			path = DATA_PATH+'/'+file

			# make sure document is not already indexed
			if indexedDocs.get(path[-20:]) is not None:
				continue

			author, title, tokens, url, published, lenText = readFile(path)
			# converting published string into required datetime format
			published = published[0:10]+" "+published[11:23]+"000"

			# make tokens for short barreling
			smalltokens = clean(author+" "+title)

			# make tokens for long barreling
			tokens = clean(tokens)

			# get wordID and docID for short barrels
			self.lexicon.wordID = self.lexicon.processFile(self.lexicon,
				self.lexicon.wordID, smalltokens)

			self.forwardIndexer.processFile(self.lexicon, shortforwardBarrels,
				BARREL_LENGTH, smalltokens, self.docID,True)

			# get wordID and dicID for large barrels
			self.lexicon.wordID = self.lexicon.processFile(self.lexicon, self.lexicon.wordID, tokens)
			self.forwardIndexer.processFile(self.lexicon, forwardBarrels, BARREL_LENGTH, tokens, self.docID)
			indexedDocs[path[-20:]] = self.docID
			
			# store document's metadata
			self.addMetadata(self.docID, author, title, url,published, lenText)
			print(self.docID)
			self.docID+=1

		print(datetime.now(), "Writing forward index to file")
		
		# dump short barrels 
		self.forwardIndexer.dump(DICT_PATH, shortforwardBarrels, overwrite=False, short=True)

		for i, file in enumerate(os.listdir(os.path.join(DICT_PATH,'short_forward_barrels'))):
			self.invertedIndexer.processFile(DICT_PATH, file, i,True)
		
		# dump long barrels
		self.forwardIndexer.dump(DICT_PATH, forwardBarrels, overwrite=False)

		print(datetime.now(), "Generating inverted index")
		for i, file in enumerate(os.listdir(os.path.join(DICT_PATH,'forward_barrels'))):
			self.invertedIndexer.processFile(DICT_PATH, file, i)

		print(datetime.now(), "Indexing complete")

	def addMetadata(self, docID, author, title, url,published,lenText):
		self.metadata[docID] = [author, title, url, published, lenText]

	def	loadIndexedDocs(self):
		try:
			with open(os.path.join(DICT_PATH, 'indexed_docs.json'), 'r', encoding="utf8") as f:
				indexedDocs = json.load(f)
		except FileNotFoundError:
			indexedDocs = dict()
		return indexedDocs

	def loadMetadata(self):
		try:
			with open(os.path.join(DICT_PATH, 'metadata.json'), 'r', encoding="utf8") as f:
				metadata = json.load(f)
		except FileNotFoundError:
			metadata = dict()
		return metadata