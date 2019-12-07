import json
import os
import string
from tqdm import tqdm
from unidecode import unidecode


# if a lexicon already exists, load it. Otherwise create new lexicon
try:
	with open('../dicts/lexicon.json', 'r', encoding="utf8") as lexfile:
		lexicon = json.load(lexfile)
	wordID = lexicon[list(lexicon.keys())[-1]] + 1      # get the last wordID in the lexicon,
														# add 1 to get wordID for next addition
except FileNotFoundError:
	lexicon = dict()
	wordID = 0

def processFile(file):
	"""
	parameters: file - path to file from which lexicon is to be generated

	Everytime this function is called, words from another clean file will
	be added to the lexicon.

	return: void
	"""
	with open(file, 'r') as f:
		tokens = f.read()

	tokens = tokens.split()

	# if the word is not already present in lexicon, add it
	global lexicon, wordID
	for token in tokens:
		if lexicon.get(token) == None:
			lexicon[token] = wordID
			wordID+=1

def generateLexicon(cleanDir, dictDir):
	"""
	parameters: cleanDir - the path of the directory containing
	processed documents.

	This function will iterate through every file in the given
	cleaned directory and add new words found to the lexicon.

	The lexicon is a dictionary of the form:
	{
		"token" : wordID,
		...
	}

	return: void
	"""
	for file in tqdm(os.listdir(cleanDir)):
		processFile(os.path.join(cleanDir, file))

	global lexicon
	with open(os.path.join(dictDir, 'lexicon.json'), 'w', encoding="utf8") as lexfile:
		json.dump(lexicon, lexfile, indent=2)