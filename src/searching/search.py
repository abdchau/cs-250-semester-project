import json
import os
import string

def searchword(dictDir,barrel_length,word):

	docIDs = []
	inverted = dict()
	with open(os.path.join(dictDir, 'lexicon.json'), 'r', encoding="utf8") as lexFile:
			lexicon = json.load(lexFile)

	wordID = lexicon[word]
	print(wordID)

	barrel = wordID//barrel_length
	print(barrel)
	path = os.path.join(dictDir, 'inverted_barrels')

	with open(os.path.join(path, f"inverted_{barrel}.json"), 'r', encoding = "utf8") as invBarrel:
		inverted = json.load(invBarrel)

	docIDs = list(inverted[str(wordID)].keys())

	print(docIDs)