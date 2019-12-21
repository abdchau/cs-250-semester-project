import json
import os
from tqdm import tqdm


class ForwardIndexer:
	# def __init__(self):
	# 	self.docID = 


	def getHits(self, listOfElements, element):
	    ''' Returns the indexes of all occurrences of give element in
	    the list- listOfElements '''
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
	 
	    return indexPosList


	def processFile(self, lexicon, forwardBarrels, barrelLength, tokens, docID,short = False):
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
			- barrelLength: the range of words in one barrel
			- tokens: the cleaned words in the file
			- docID: the unique ID assigned to the file

		This function will add hits for every word present in
		the file to the correct dictionary according to barrel
		number, docID and wordID.

		returns: None
		"""
		tokens = [lexicon.lexDict[token] for token in tokens]

		wordIDs = set(tokens)

		for wordID in wordIDs:

			# choose barrel
			barrel = wordID//barrelLength

			# prepare dictionary for hits insertion
			if forwardBarrels.get(barrel) is None:
				forwardBarrels[barrel] = dict()
			if forwardBarrels[barrel].get(docID) is None:
				forwardBarrels[barrel][docID] = dict()

			# insert the hits
			hits = self.getHits(tokens, wordID)
			hits.insert(0,len(hits))
			forwardBarrels[barrel][docID][wordID] = hits


	def addFile(self, dictDir, lexicon, tokens, docID, barrels, barrelLength,short=False):
		"""
		arguments:
			- dictDir: the path of the directory containing the
			dictionaries for the forward and the inverted index
			- lexicon: the lexicon to be used for indexing
			- tokens: the cleaned words in the file
			- barrels: the barrel numbers that are to be updated
			- barrelLength: the range of words in one barrel

		This function simply loads the barrels specified, forms
		the forwardBarrels dictionary as required by the
		processFile function and then passes everything on to
		processFile(). After the barrels have been updated, it
		dumps them to file.

		return: the updated forward barrels and the docID assigned
		to the new file
		"""
		forwardBarrels = dict()
		folder = 'forward_barrels'
		if short:
			folder = 'short_forward_barrels'

		path = os.path.join(dictDir, folder)
		os.makedirs(path, exist_ok=True)
		for barrel in barrels:
			try:
				with open(os.path.join(path, f'forward_{barrel}.json'), 'r', encoding = "utf8") as forwardFile:
					forwardBarrels[barrel] = json.load(forwardFile)
			except:
				forwardBarrels[barrel] = dict()

		self.processFile(lexicon, forwardBarrels, barrelLength, tokens, docID, short)
		self.dump(dictDir, forwardBarrels,short)
		return forwardBarrels


	def dump(self, dictDir, forwardBarrels, overwrite=True, short=False):
		"""
		arguments:
			- dictDir: the path of the directory containing the
			dictionaries for the lexicon and the forward index
			- forwardBarrels: the dictionary in which the forward
			indices are stored. The form is described above

		This function will iterate through the forward barrels
		and will write each to file.

		return: None
		"""
		folder = 'forward_barrels'
		if short:
			folder = 'short_forward_barrels'
		path = os.path.join(dictDir, folder)
		os.makedirs(path, exist_ok=True)
		for barrel, forwardIndex in forwardBarrels.items():
			print(barrel)
			temp = dict()
			if not overwrite:
				try:
					with open(os.path.join(path, f'forward_{barrel}.json'), 'r', encoding = "utf8") as forwardFile:
						temp = json.load(forwardFile)
						if temp is None:
							temp = dict()
				except FileNotFoundError:
					pass
			temp.update(forwardIndex)
			with open(os.path.join(path, f'forward_{barrel}.json'), 'w', encoding = "utf8") as forwardFile:
				json.dump(temp, forwardFile, indent=2)