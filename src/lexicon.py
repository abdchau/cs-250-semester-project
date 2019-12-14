import json
import os
import string
from tqdm import tqdm
from unidecode import unidecode


def processFile(lexicon, wordID, tokens):
	"""
	arguments:
		- file: path to file from which lexicon is
		to be generated

	Everytime this function is called, words from another clean file will
	be added to the lexicon.

	return: void
	"""

	# if the word is not already present in lexicon, add it
	for token in tokens:
		if lexicon.get(token) == None:
			lexicon[token] = wordID
			wordID+=1

	return wordID

def generateLexicon(cleanDir, dictDir):
	"""
	arguments:
		- cleanDir: the path of the directory containing
		processed documents.

	This function will iterate through every file in the given
	cleaned directory and add new words found to the lexicon.

	The lexicon is a dictionary of the form:
	{
		"token" : wordID,
		...
	}

	return: None
	"""
	for file in tqdm(os.listdir(cleanDir)):
		processFile(os.path.join(cleanDir, file))

	global lexicon
	with open(os.path.join(dictDir, 'lexicon.json'), 'w', encoding="utf8") as lexfile:
		json.dump(lexicon, lexfile, indent=2)

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
		wordID = lexicon[list(lexicon.keys())[-1]] + 1      # get the last wordID in the lexicon,
															# add 1 to get wordID for next addition
	except FileNotFoundError:
		lexicon = dict()
		wordID = 0

	return lexicon, wordID

def dump(dictDir, lexicon):
	with open(os.path.join(dictDir, 'lexicon.json'), 'w', encoding="utf8") as lexFile:
		json.dump(lexicon, lexFile, indent=2)