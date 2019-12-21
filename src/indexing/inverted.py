import json
import os
import string
from tqdm import tqdm


class InvertedIndexer:
	"""docstring for InvertedIndexer"""
		

	def processFile(self, dictDir, forwardFile, barrel, short=False):
		"""
		arguments:
			- dictDir: the path of the directory containing the
			dictionaries for the forward and the inverted index
			- forwardFile: the path to the forward barrel that
			is to be inverted
			- barrel: the barrel number being inverted

		This function will iterate through every wordID in the
		barrel's range. For every wordID, it will subsequently
		iterate through every docID in the forward barrel, and
		will generate a dictionary containing the hits of that 
		wordID in each document.

		This dictionary will then be added to the inverted index
		barrel, which will be written to file.

		The inverted index is a dictionary of dictionaries of the form:
		{
			wordID : 
				{
					docID : [
						location of first hit,
						location of second hit,
						...
					],
					...
				},
			...
		}

		return: None
		"""
		invertedIndex = dict()
		folder = 'forward_barrels'
		if short:
			folder = 'short_forward_barrels'

		# get all docIDs from forward barrel
		with open(os.path.join(dictDir+"/"+folder, forwardFile), 'r', encoding="utf8") as fIndex:
			forward = json.load(fIndex)
		docIDs = list(forward.keys())


		for docID in tqdm(docIDs):

			# if word occurs in some document, record 'inverted' hits
			for wordID in forward[docID].keys():

				if invertedIndex.get(wordID) is None:
					invertedIndex[wordID] = dict()
				if invertedIndex[wordID].get(docID) is None:
					invertedIndex[wordID][docID] = dict()

				invertedIndex[wordID][docID] = forward[docID][str(wordID)]

		# dump inverted barrel to file
		folder = 'inverted_barrels'
		if short:
			folder = 'short_inverted_barrels'
		path = os.path.join(dictDir, folder)
		os.makedirs(path, exist_ok=True)


		with open(os.path.join(path, f"inverted_{barrel}.json"), 'w', encoding = "utf8") as invBarrel:
			json.dump(invertedIndex, invBarrel, indent=2)


	def addFile(self, dictDir, wordIDs, docID, barrels, forwardBarrels, short=False):
		"""
		arguments:
			- dictDir: the path of the directory containing the
			dictionaries for the forward and the inverted index
			- wordIDs: a sorted list of unique wordIDs that were
			present in the new file being indexed
			- docID: the docID assigned to the new file
			- barrels: the barrel numbers that are to be updated
			- forwardBarrels: a dictionary containing the forward
			index barrels that have been updated prior to this
			function being called

		This function will iterate through every barrel that it
		has been instructed to update, and will add the 'inverted
		hits' to it. The function avoids having to iterate over
		all wordIDs for every barrel by checking if the wordID
		is present in the corresponding forward barrel.

		Once a wordID is found that is not present in current
		barrel, we remove all the wordIDs that have been added
		and move to the next barrel. The sorted property of the
		wordIDs list guarantees that once a wordID is not found
		it is safe to move to the next barrel.

		The wordIDs that have been removed were removed so
		that the next barrel would not be simply skipped
		because these IDs will obviously not be present in
		the corresponding next forward barrel.

		return: None
		"""
		folder = 'inverted_barrels'
		if short:
			folder = 'short_inverted_barrels'
		path = os.path.join(dictDir, folder)
		os.makedirs(path, exist_ok=True)

		for barrel in barrels:
			# open inverted barrel
			try:
				with open(os.path.join(path, f"inverted_{barrel}.json"), 'r', encoding = "utf8") as invBarrel:
					invertedIndex = json.load(invBarrel)
			except:
				invertedIndex = dict()

			rem = []
			for wordID in wordIDs:
				# if word occurs in some barrel, record 'inverted' hits
				hits = forwardBarrels[barrel][str(docID)].get(wordID)

				if hits is not None:
					if invertedIndex.get(str(wordID)) is None:
						invertedIndex[str(wordID)] = dict()
					invertedIndex[str(wordID)][docID] = hits
					rem.append(wordID)
				else:
					# remove indexed words from list
					for wordID in rem:
						wordIDs.remove(wordID)
					rem = []
					break

			# dump updated barrel to file
			with open(os.path.join(path, f"inverted_{barrel}.json"), 'w', encoding = "utf8") as invBarrel:
				json.dump(invertedIndex, invBarrel, indent=2)