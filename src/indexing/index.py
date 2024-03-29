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

		self.forwardIndexer = ForwardIndexer(self.indexedDocs)
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
		if self.indexedDocs.get(file[-21:]) is not None:
			print(datetime.now(), "Document already present in index.")
			return

		print(file)
		print(datetime.now(), "Adding document to index.")

		# get author name, title, all texts, url, weightedShares and file path of given file
		author, title, tokens, url, shares, filepath = readFile(file)

		# clean the texts for short and long barreling
		shortTokens = clean(author+" "+title)
		tokens = clean(tokens)

		# add tokens to lexicon
		self.lexicon.processFile(tokens)
		self.lexicon.processFile(shortTokens)

		# get unique, sorted wordIDs present in the file
		wordIDs = sorted(set([self.lexicon.lexDict[token] for token in tokens]))
		shortWordIDs = sorted(set([self.lexicon.lexDict[token] for token in shortTokens]))

		# get all barrels that are to be updated
		barrels = sorted(set([getBarrel(wordID) for wordID in wordIDs]))
		shortBarrels = sorted(set([getBarrel(wordID) for wordID in shortWordIDs]))

		# add data to long and short forward barrels
		shortForwardBarrels, _ = self.forwardIndexer.addFile(dictDir, 
			self.lexicon, shortTokens, shortBarrels, short=True)
		forwardBarrels, docID = self.forwardIndexer.addFile(dictDir, 
			self.lexicon, tokens, barrels)

		# add data to long and short inverted barrels
		self.invertedIndexer.addFile(dictDir, shortWordIDs, docID, shortBarrels, shortForwardBarrels, short=True)
		self.invertedIndexer.addFile(dictDir, wordIDs, docID, barrels, forwardBarrels)

		print(datetime.now(), "Document added to index.")
		
		# add documentID into indexedDocs so it is not indexed again
		self.indexedDocs[file[-21:]] = docID

		# store document's metadata
		self.addMetadata(docID, author, title, url,shares,filepath)
		print(docID)
		forwardBarrels.clear()


	def indexDataset(self):
		"""
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
				if self.indexedDocs.get(path[-21:]) is not None:
					continue

				# get author name, title, all texts, url, weightedShares and file path of given file
				author, title, tokens, url, shares, filepath = readFile(path)
				
				
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
				self.indexedDocs[path[-21:]] = self.forwardIndexer.docID-1
			
				# store document's metadata
				self.addMetadata(self.forwardIndexer.docID-1, author, title, url,shares, filepath)

		
		# dump short barrels 
		print(datetime.now(), "Writing short forward index to file.")
		self.forwardIndexer.dump(DICT_PATH, shortForwardBarrels, overwrite=False, short=True)

		# dump long barrels
		print(datetime.now(), "Writing long forward index to file.")
		self.forwardIndexer.dump(DICT_PATH, forwardBarrels, overwrite=False)
		forwardBarrels.clear()

		# invert short barrels
		print(datetime.now(), "Generating short inverted index.")
		for file in os.listdir(os.path.join(DICT_PATH,'short_forward_barrels')):
			self.invertedIndexer.processFile(DICT_PATH, file, int(file[8:-5]), short=True)

		# invert long barrels
		print(datetime.now(), "Generating long inverted index.")
		for file in os.listdir(os.path.join(DICT_PATH,'forward_barrels')):
			self.invertedIndexer.processFile(DICT_PATH, file, int(file[8:-5]))

		print(datetime.now(), "Indexing complete.")


	def addMetadata(self, docID, author, title, url,shares,filepath):
		# store arguments in metadata dictionary
		self.metadata[str(docID)] = [title, author, url,shares,filepath]


	def	loadIndexedDocs(self):

		# load and return indexedDocs
		try:
			with open(os.path.join(DICT_PATH, 'indexed_docs.json'), 'r', encoding="utf8") as f:
				indexedDocs = json.load(f)
		except FileNotFoundError:
			indexedDocs = dict()
		return indexedDocs


	def loadMetadata(self):

		# load and return metadata
		try:
			with open(os.path.join(DICT_PATH, 'metadata.json'), 'r', encoding="utf8") as f:
				metadata = json.load(f)
		except FileNotFoundError:
			metadata = dict()
		return metadata