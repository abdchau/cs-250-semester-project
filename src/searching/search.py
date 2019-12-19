import json
import os
import string
from config import *

def searchword(dictDir,barrel_length,word):

	docIDs = []
	inverted = dict()
	with open(os.path.join(dictDir, 'lexicon.json'), 'r', encoding="utf8") as lexFile:
			lexicon = json.load(lexFile)

	wordID = lexicon[word]

	barrel = wordID//barrel_length

	path = os.path.join(dictDir, 'inverted_barrels')

	with open(os.path.join(path, f"inverted_{barrel}.json"), 'r', encoding = "utf8") as invBarrel:
		inverted = json.load(invBarrel)

	docIDs = list(inverted[str(wordID)].keys())
	hitsIndex = dict()
	for docID in docIDs:
		hitsIndex[docID] = inverted[str(wordID)][str(docID)]

	sortedKeys = sorted(hitsIndex, key=lambda key:hitsIndex[key][0], reverse=True)
	hitsIndex = {k:hitsIndex[k] for k in sortedKeys}
	print(hitsIndex)
	return hitsIndex
	
# def sortHits(numberofHits);
	