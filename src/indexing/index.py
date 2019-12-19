from tqdm import tqdm
import os
from indexing import lexicon as L
from indexing import forward
from indexing import inverted
from indexing.cleanText import *
from datetime import datetime
from config import *


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
		print("return")
		return
	print(indexedDocs)
	print(file)
	print("not return")

	author, title, tokens, url, published, lenText = readFile(path)

	smalltokens = clean(author+" "+title)
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
	addMetadata(docID, author, title, url,published,lenText)
	# print(metadata)

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
	shortforwardBarrels = dict()
	forwardBarrels = dict()
	wordID = L.getNewWordID()
	for file in tqdm(os.listdir(DATA_PATH)):
		path = DATA_PATH+'/'+file

		# make sure document is not already indexed
		if indexedDocs.get(path[-20:]) is not None:
			continue

		author, title, tokens, url, published, lenText = readFile(path)
		#converting published string into required datetime format
		published = published[0:10]+" "+published[11:23]+"000"
		#make tokens for short barreling
		smalltokens = clean(author+" "+title)
		#make tokens for long barreling
		tokens = clean(tokens)
		#get wordID and  docID for short barrels
		wordID = L.processFile(lexicon, wordID, smalltokens)
		docID = forward.processFile(lexicon, shortforwardBarrels, BARREL_LENGTH, smalltokens, docID_[0],True)
		#get wordID and dicID for large barrels
		wordID = L.processFile(lexicon, wordID, tokens)
		docID = forward.processFile(lexicon, forwardBarrels, BARREL_LENGTH, tokens, docID_[0])
		indexedDocs[path[-20:]] = docID
		
		# store document's metadata
		addMetadata(docID, author, title, url,published, lenText)

	#dump lexicon
	print(datetime.now(), "Writing lexicon and forward index to file")
	L.dump(DICT_PATH, lexicon)
	
	#dump short forward and inverted barrels 
	forward.dump(DICT_PATH, shortforwardBarrels, overwrite=False, short=True)

	for i, file in enumerate(os.listdir(os.path.join(DICT_PATH,'short_forward_barrels'))):
		inverted.processFile(DICT_PATH, file, i,True)
	
	#dump the big barrels
	forward.dump(DICT_PATH, forwardBarrels, overwrite=False)

	print(datetime.now(), "Generating inverted index")
	for i, file in enumerate(os.listdir(os.path.join(DICT_PATH,'forward_barrels'))):
		inverted.processFile(DICT_PATH, file, i)

	print(datetime.now(), "Indexing complete")

def addMetadata(docID, author, title, url,published,lenText):
	metadata[docID] = [author, title, url,published,lenText]