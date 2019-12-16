import json
import os
import string
from tqdm import tqdm


def processFile(dictDir, forwardFile, barrel):
	"""
	arguments:
		- dictDir: the path of the directory containing the
		dictionaries for the forward and the inverted index.
		- forwardFile: the path to the forward barrel that is
		to be inverted
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
					number of hits in this document,
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
	
	# get all docIDs from forward barrel
	with open(os.path.join(dictDir+"\\forward_barrels", forwardFile), 'r', encoding="utf8") as fIndex:
		forward = json.load(fIndex)
	docIDs = list(forward.keys())


	for docID in tqdm(docIDs):

		# if word occurs in some document, record 'inverted' hits
		for wordID in list(forward[docID].keys()):
			if forward[docID].get(str(wordID)) is None:
				continue

			if invertedIndex.get(wordID) is None:
				invertedIndex[wordID] = dict()
			if invertedIndex[wordID].get(docID) is None:
				invertedIndex[wordID][docID] = dict()

			invertedIndex[wordID][docID] = forward[docID][str(wordID)]

	# dump inverted barrel to file
	path = os.path.join(dictDir, 'inverted_barrels')
	os.makedirs(path, exist_ok=True)

	with open(os.path.join(path, f"inverted_{barrel}.json"), 'w', encoding = "utf8") as invBarrel:
		json.dump(invertedIndex, invBarrel, indent=2)

def addFile(dictDir, wordIDs, docID, barrels, forwardBarrels):
	path = os.path.join(dictDir, 'inverted_barrels')
	os.makedirs(path, exist_ok=True)

	for barrel in barrels:
		with open(os.path.join(path, f"inverted_{barrel}.json"), 'r', encoding = "utf8") as invBarrel:
			invertedIndex = json.load(invBarrel)

		rem = []
		for wordID in wordIDs:
			hits = forwardBarrels[barrel][str(docID)].get(wordID)

			if hits is not None:
				if invertedIndex.get(str(wordID)) is None:
					invertedIndex[str(wordID)] = dict()
				invertedIndex[str(wordID)][docID] = hits
				rem.append(wordID)
			else:
				for wordID in rem:
					wordIDs.remove(wordID)
				rem = []
				break

		with open(os.path.join(path, f"inverted_{barrel}.json"), 'w', encoding = "utf8") as invBarrel:
			json.dump(invertedIndex, invBarrel, indent=2)