import json
import os
import string
from tqdm import tqdm
from config import DICT_PATH


class Lexicon:
	def __init__(self, dictDir):
		# create new lexicon
		self.lexDict = dict()
		self.wordID = 1
		self.loadLexicon(dictDir)


	def processFile(self, tokens):
		"""
		arguments:
			- tokens: the 'cleaned' text from the file being
			processed

		Everytime this function is called, words from another
		clean file will	be added to the lexicon.

		return: None
		"""
		for token in tokens:
			# if the word is not already present in lexicon, add it
			if self.lexDict.get(token) == None:
				self.lexDict[token] = self.wordID
				self.wordID+=1


	def loadLexicon(self, dictDir):
		"""
		arguments: 
			- dictDir: the path of the directory containing the
			lexicon.

		This function reads the lexicon from file. If the file
		does not exist, it retains the new lexicon.

		return: None
		"""
		try:
			with open(os.path.join(dictDir, 'lexicon.json'), 'r', encoding="utf8") as lexFile:
				self.lexDict = json.load(lexFile)
			self.wordID = self.lexDict[list(self.lexDict.keys())[-1]] + 1	# get the last wordID in the lexicon,
																			# add 1 to get wordID for next addition
		except FileNotFoundError:
			pass


	def dump(self):
		with open(os.path.join(DICT_PATH, 'lexicon.json'), 'w', encoding="utf8") as lexFile:
			json.dump(self.lexDict, lexFile, indent=2)