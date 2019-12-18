from tqdm import tqdm
import os
from indexing import lexicon as L
from indexing import forward
from indexing import inverted
from indexing.cleanText import *
from datetime import datetime
from config import DATA_PATH, DICT_PATH, BARREL_LENGTH


try:
	with open(os.path.join(DICT_PATH, 'indexed_docs.json'), 'r', encoding="utf8") as f:
		indexedDocs = json.load(f)
except FileNotFoundError:
	indexedDocs = dict()

try:
	with open(os.path.join(DICT_PATH, 'metadata.json'), 'r', encoding="utf8") as f:
		metadata = json.load(f)
except FileNotFoundError:
	metadata = dict()


def addFile(dictDir, file, lexicon, barrelLength):
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
		return

	author, title, tokens, url = readFile(file)
	tokens = clean(tokens)
	L.processFile(lexicon, L.getNewWordID(), tokens)

	# get unique, sorted wordIDs present in the file
	wordIDs = sorted(set([lexicon[token] for token in tokens]))

	# get all barrels that are to be updated
	barrels = sorted(set([wordID//barrelLength for wordID in wordIDs]))

	forwardBarrels, docID = forward.addFile(dictDir, lexicon, tokens, barrels, barrelLength)
	inverted.addFile(dictDir, wordIDs, docID, barrels, forwardBarrels)
	L.dump(dictDir, lexicon)
	indexedDocs[file[-20:]] = docID

	# store document's metadata
	addMetadata(docID, author, title, url)
	print(metadata)

def indexDataset(lexicon):
	"""
	arguments:
		- lexicon: the main lexicon that is to be held
		in memory

	This function will iterate over the dataset provided
	in DATASET_PATH and will index it. The indexes and
	lexicon will be written to the DICT_PATH directory.

	return: None
	"""
	print(datetime.now(), "Generating lexicon and forward index")

	forwardBarrels = dict()
	wordID = L.getNewWordID()
	for file in tqdm(os.listdir(DATA_PATH)[1:2]):
		path = os.path.join(DATA_PATH, file)

		# make sure document is not already indexed
		if indexedDocs.get(path[-20:]) is not None:
			continue

		author, title, tokens, url = readFile(path)
		print(author)
		tokens = clean(tokens)

		wordID = L.processFile(lexicon, wordID, tokens)
		docID = forward.processFile(lexicon, forwardBarrels, BARREL_LENGTH, tokens, forward.docID_[0])
		indexedDocs[path[-20:]] = forward.docID_[0]
		
		# store document's metadata
		addMetadata(docID, author, title, url)

	# print(metadata)
	print(datetime.now(), "Writing lexicon and forward index to file")
	L.dump(DICT_PATH, lexicon)
	# print(forwardBarrels)
	forward.dump(DICT_PATH, forwardBarrels, overwrite=False)

	print(datetime.now(), "Generating inverted index")
	for i, file in enumerate(os.listdir(os.path.join(DICT_PATH,'forward_barrels'))):
		inverted.processFile(DICT_PATH, file, i)

	print(datetime.now(), "Indexing complete")

def addMetadata(docID, author, title, url):
	metadata[docID] = [author, title, url]