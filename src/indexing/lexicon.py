import json
import os
import string
from tqdm import tqdm
from config import DICT_PATH


class Lexicon:
	def __init__(self, dictDir):
		self.lexDict, self.wordID = self.loadLexicon(dictDir)


	def processFile(self, lexicon, wordID, tokens):
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
			if self.lexDict.get(token) == None:
				self.lexDict[token] = wordID
				wordID+=1

		return wordID


	# def getNewWordID(self):
	# 	return wordID_[0]

	def loadLexicon(self, dictDir):
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
				self.lexDict = json.load(lexFile)
			wordID = self.lexDict[list(self.lexDict.keys())[-1]] + 1		# get the last wordID in the lexicon,
																# add 1 to get wordID for next addition
		except FileNotFoundError:
			self.lexDict = dict()
			wordID = 1
		return self.lexDict, wordID


	def dump(self):
		with open(os.path.join(DICT_PATH, 'lexicon.json'), 'w', encoding="utf8") as lexFile:
			json.dump(self.lexDict, lexFile, indent=2)