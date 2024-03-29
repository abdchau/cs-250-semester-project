import numpy as np
import json
import os
from tqdm import tqdm
from indexing.helper import *


class ForwardIndexer:
	def __init__(self, indexedDocs):
		self.docID = 100000
		if indexedDocs:
			self.docID = int(list(indexedDocs.values())[-1])+1

	def getPositonDecay(self, listOfElements, element):
		''' Returns an integer as positionDecay which represents the significance of element
			by first getting all occurrence of the element then mapping all the occurence 
			in such a way that occurences closer to start will have a higher value than
			the rest, then sum all the mapped numbers.'''
		indexPosList = []
		indexPos = 0
		while True:
			try:
				# Search for item in list from indexPos to the end of list
				indexPos = listOfElements.index(element, indexPos)
				# Add the index position in list
				indexPosList.append(indexPos)
				indexPos += 1
			except ValueError as e:
				break
		
		# map all the position and add them up
		f = lambda position: 0.999**position
		positionDecay = np.sum(f(np.array(indexPosList)))

		return int(positionDecay*100)


	def processFile(self, lexicon, forwardBarrels, tokens, short=False):
		"""
		arguments:
			- lexicon: the lexicon to be used for indexing
			- forwardBarrels: the dictionary in which the forward
			indices are to be stored. Each forward index is of 
			the form:
			{
				docID : 
					{
						wordID : [
							location of first hit,
							location of second hit,
							...
						],
						...
					},
				...
			}
			- tokens: the cleaned words in the file
			- short: whether or not the file is being processed
			for short barrels

		This function will add positionDeccay for every word present in
		the file to the correct dictionary according to barrel
		number, docID, short and wordID.

		returns: None
		"""
		tokens = [lexicon.lexDict[token] for token in tokens]

		wordIDs = set(tokens)

		for wordID in wordIDs:

			# choose barrel and make the next barrel with twice as many unique wordIDs
			barrel = getBarrel(wordID)

			# prepare dictionary for positionDecay insertion
			if forwardBarrels.get(barrel) is None:
				forwardBarrels[barrel] = dict()
			if forwardBarrels[barrel].get(str(self.docID)) is None:
				forwardBarrels[barrel][str(self.docID)] = dict()

			# insert the positionDecay
			positionDecay = self.getPositonDecay(tokens, wordID)
			
			forwardBarrels[barrel][str(self.docID)][wordID] = positionDecay

		# increase docID if the processing is not for short barrels
		if not short:
			self.docID+=1


	def addFile(self, dictDir, lexicon, tokens, barrels, short=False):
		"""
		arguments:
			- dictDir: the path of the directory containing the
			dictionaries for the forward and the inverted index
			- lexicon: the lexicon to be used for indexing
			- tokens: the cleaned words in the file
			- barrels: the barrel numbers that are to be updated
			- short: whether or not the file is being processed
			for short barrels 

		This function simply loads the barrels specified, forms
		the forwardBarrels dictionary as required by the
		processFile function and then passes everything on to
		processFile(). After the barrels have been updated, it
		dumps them to file.

		return: the updated forward barrels and the docID assigned
		to the new file
		"""
		forwardBarrels = dict()

		# change destination folder if processing is for short barrels
		folder = 'forward_barrels'
		if short:
			folder = 'short_forward_barrels'

		# get path by joining dictDir and folder
		path = os.path.join(dictDir, folder)
		os.makedirs(path, exist_ok=True)

		# load all forward barrels that are to be updated
		for barrel in barrels:
			try:
				with open(os.path.join(path, f'forward_{barrel}.json'), 'r', encoding = "utf8") as forwardFile:
					forwardBarrels[barrel] = json.load(forwardFile)
			except:
				forwardBarrels[barrel] = dict()

		# process and dump all the barrels loaded
		self.processFile(lexicon, forwardBarrels, tokens, short=short)
		self.dump(dictDir, forwardBarrels, short=short)
		return forwardBarrels, self.docID-1


	def dump(self, dictDir, forwardBarrels, overwrite=True, short=False):
		"""
		arguments:
			- dictDir: the path of the directory containing the
			dictionaries for the lexicon and the forward index
			- forwardBarrels: the dictionary in which the forward
			indices are stored. The form is described above
			-overwrite: tells whether files are to be overwritten
			- short: whether or not the file is being processed
			for short barrels

		This function will iterate through the forward barrels
		and will write each to file.

		return: None
		"""

		# change destination folder if processing is for short barrels
		folder = 'forward_barrels'
		if short:
			folder = 'short_forward_barrels'

		# get path by joining dictDir and folder	
		path = os.path.join(dictDir, folder)
		os.makedirs(path, exist_ok=True)

		# split forwardBarrel to keys: (berrel number) and value:(forwardIndex)

		for barrel, forwardIndex in forwardBarrels.items():
			print(barrel)
			temp = dict()

			# do processing if overwrite is false
			if not overwrite:
				try:
					with open(os.path.join(path, f'forward_{barrel}.json'), 'r', encoding = "utf8") as forwardFile:
						temp = json.load(forwardFile)
						if temp is None:
							temp = dict()
				except FileNotFoundError:
					pass

			# merge temp dictionary with forwardIndex then dump the temp dictionary into file		
			temp.update(forwardIndex)
			with open(os.path.join(path, f'forward_{barrel}.json'), 'w', encoding = "utf8") as forwardFile:
				json.dump(temp, forwardFile, indent=2)
			temp.clear()
		# forwardBarrels.clear()