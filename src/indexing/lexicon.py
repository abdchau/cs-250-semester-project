import json
import os
import string
from tqdm import tqdm


def processFile(lexicon, wordID, tokens):
	"""
	arguments:
		- lexicon: the lexicon to which words are to be
		added
		- wordID: the wordID to be assigned to the first
		new word found
		- tokens: the 'cleaned' text from the file being
		processed

	Everytime this function is called, words from another
	clean file will	be added to the lexicon.

	return: the wordID that must be assigned to whatever
	word is next added to this lexicon
	"""

	# if the word is not already present in lexicon, add it
	for token in tokens:
		if lexicon.get(token) == None:
			lexicon[token] = wordID
			wordID+=1

	return wordID


def getNewWordID(lexicon):
	if lexicon:
		return lexicon[list(lexicon.keys())[-1]] + 1
	else:
		return 0

def load(dictDir):
	"""
	arguments: 
		- dictDir: the path of the directory containing the
		lexicon.

	This function reads the lexicon from file. If the file
	does not exist, it initializes a new lexicon.

	return: a dictionary containing the loaded/new lexicon
	"""
	try:
		with open(os.path.join(dictDir, 'lexicon.json'), 'r', encoding="utf8") as lexFile:
			lexicon = json.load(lexFile)
		wordID = getNewWordID(lexicon) # get the last wordID in the lexicon,
															# add 1 to get wordID for next addition
	except FileNotFoundError:
		lexicon = dict()
		wordID = 0

	return lexicon, wordID


def dump(dictDir, lexicon):
	with open(os.path.join(dictDir, 'lexicon.json'), 'w', encoding="utf8") as lexFile:
		json.dump(lexicon, lexFile, indent=2)