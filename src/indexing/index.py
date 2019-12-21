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
		self.lexicon = Lexicon(DICT_PATH)

		self.indexedDocs = self.loadIndexedDocs()
		self.metadata = self.loadMetadata()

		self.forwardIndexer = ForwardIndexer()
		self.invertedIndexer = InvertedIndexer()
		

	def addFile(self, dictDir, file):
		"""
		arguments:
			- dictDir: the path of the directory containing the
			dictionaries for the forward and the inverted index
			- file: the path to the file that is to be added

		This function updates the lexicon to accommodate the
		new file and adds the file to the forward and inverted
		indexes.

		return: None
		"""

		# if document is already indexed, return
		if indexedDocs.get(file[-21:]) is not None:
			print(datetime.now(), "Document already present in index.")
			return

		print(file)
		print(datetime.now(), "Adding document to index.")

		author, title, tokens, url, published = readFile(file)

		shortTokens = clean(author+" "+title)
		tokens = clean(tokens)

		self.lexicon.wordID = self.lexicon.processFile(tokens)

		# get unique, sorted wordIDs present in the file
		wordIDs = sorted(set([self.lexicon.lexDict[token] for token in tokens]))

		# get all barrels that are to be updated
		barrels = sorted(set([getBarrel(wordID) for wordID in wordIDs]))

		# add data to long and short forward barrels
		shortForwardBarrels, _ = self.forwardIndexer.addFile(dictDir, 
			self.lexicon, shortTokens, barrels, short=True)
		forwardBarrels, docID = self.forwardIndexer.addFile(dictDir, 
			self.lexicon, tokens, barrels)

		# add data to long and short inverted barrels
		self.invertedIndexer.addFile(dictDir, wordIDs, docID, barrels, shortForwardBarrels, short=True)
		self.invertedIndexer.addFile(dictDir, wordIDs, docID, barrels, forwardBarrels)

		print(datetime.now(), "Document added to index.")
		
		indexedDocs[file[-21:]] = docID

		# store document's metadata
		self.addMetadata(docID, author, title, url, published)
		print(docID)


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
		shortForwardBarrels = dict()
		forwardBarrels = dict()

		print(datetime.now(), "Generating lexicon and forward index.")

		for folder in os.listdir(DATA_PATH): 
			FILE_PATH = DATA_PATH+'/'+folder
			for file in tqdm(os.listdir(FILE_PATH)):
				path = FILE_PATH+'/'+file

				# make sure document is not already indexed
				if indexedDocs.get(path[-21:]) is not None:
					continue

				author, title, tokens, url, published = readFile(path)
				# converting published string into required datetime format
				published = published[0:10]+" "+published[11:23]+"000"

				# make tokens for long and short barreling
				shortTokens = clean(author+" "+title)
				tokens = clean(tokens)

				# add tokens to lexicon
				self.lexicon.processFile(shortTokens)
				self.lexicon.processFile(tokens)

				# index short barrels
				self.forwardIndexer.processFile(self.lexicon, shortForwardBarrels, shortTokens, short=True)

				# index long barrels
				self.forwardIndexer.processFile(self.lexicon, forwardBarrels, tokens)

				# record that document has been indexed
				indexedDocs[path[-21:]] = self.forwardIndexer.docID-1
			
				# store document's metadata
				self.addMetadata(self.forwardIndexer.docID-1, author, title, url,published)

		
		# dump short barrels 
		print(datetime.now(), "Writing short forward index to file.")
		self.forwardIndexer.dump(DICT_PATH, shortForwardBarrels, overwrite=False, short=True)

		# dump long barrels
		print(datetime.now(), "Writing long forward index to file.")
		self.forwardIndexer.dump(DICT_PATH, forwardBarrels, overwrite=False)

		# invert short barrels
		print(datetime.now(), "Generating short inverted index.")
		for file in os.listdir(os.path.join(DICT_PATH,'short_forward_barrels')):
			self.invertedIndexer.processFile(DICT_PATH, file, int(file[8:-5]), short=True)

		# invert long barrels
		print(datetime.now(), "Generating long inverted index.")
		for file in os.listdir(os.path.join(DICT_PATH,'forward_barrels')):
			self.invertedIndexer.processFile(DICT_PATH, file, int(file[8:-5]))

		print(datetime.now(), "Indexing complete.")


	def addMetadata(self, docID, author, title, url,published):
		self.metadata[docID] = [author, title, url, published]


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