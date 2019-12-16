from tqdm import tqdm
import os
from indexing import lexicon as L
from indexing import forward
from indexing import inverted
from indexing.cleanText import clean
from datetime import datetime
from config import DATA_PATH, DICT_PATH, BARREL_LENGTH


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
	tokens = clean(file)
	L.processFile(lexicon, L.getNewWordID(lexicon), tokens)

	# get unique, sorted wordIDs present in the file
	wordIDs = sorted(set([lexicon[token] for token in tokens]))

	# get all barrels that are to be updated
	barrels = set([wordID//barrelLength for wordID in wordIDs])

	forwardBarrels, docID = forward.addFile(dictDir, lexicon, tokens, barrels, barrelLength)
	inverted.addFile(dictDir, wordIDs, docID, barrels, forwardBarrels)
	L.dump(dictDir, lexicon)


def indexDataset(lexicon):
	"""
	arguments:
		- lexicon: the main lexicon that is to be held
		in memory. It will generated from scratch

	This function will iterate over the dataset provided
	in DATASET_PATH and will index it. The indexes and
	lexicon will be written to the DICT_PATH directory.

	return: None
	"""
	print(datetime.now(), "Generating lexicon and forward index")
	
	forwardBarrels = dict()
	wordID = 0
	for docID, file in tqdm(enumerate(os.listdir(DATA_PATH)[1:2])):
		tokens = clean(os.path.join(DATA_PATH, file))

		wordID = L.processFile(lexicon, wordID, tokens)
		forward.processFile(lexicon, forwardBarrels, BARREL_LENGTH, tokens, docID+100000)

	print(datetime.now(), "Writing lexicon and forward index to file")
	L.dump(DICT_PATH, lexicon)
	forward.dump(DICT_PATH, forwardBarrels)

	print(datetime.now(), "Generating inverted index")
	for i, file in enumerate(os.listdir(os.path.join(DICT_PATH,'forward_barrels'))):
		inverted.processFile(DICT_PATH, file, i)

	print(datetime.now(), "Indexing complete")