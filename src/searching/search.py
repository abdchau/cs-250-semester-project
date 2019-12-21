import json
import os
import string
from config import *
from indexing.helper import *
from collections import Counter
from indexing.helper import *

def searchWord(dictDir,word):

	docIDs = []
	inverted = dict()
	with open(os.path.join(dictDir, 'lexicon.json'), 'r', encoding="utf8") as lexFile:
			lexicon = json.load(lexFile)

	wordID = lexicon[word]
	barrel = getBarrel(wordID)
	path = os.path.join(dictDir, 'inverted_barrels')

	with open(os.path.join(path, f"inverted_{barrel}.json"), 'r', encoding = "utf8") as invBarrel:
		inverted = json.load(invBarrel)

	docIDs = list(inverted[str(wordID)].keys())
	hitsIndex = dict()
	for docID in docIDs:
		hitsIndex[docID] = inverted[str(wordID)][str(docID)][0]

	sortedKeys = sorted(hitsIndex, key=lambda key:hitsIndex[key], reverse=True)
	hitsIndex = {k:hitsIndex[k] for k in sortedKeys}
	print("doc ids for word " + word + " and hits :")
	print(hitsIndex)
	return hitsIndex


def searchquery(dictDir,query):
	result_of_WordID = dict()
	docIDs_of_all_words = []
	words = clean(query)

	for word in words:
		result_of_WordID[word] = searchWord(dictDir,word)
		docIDs_of_all_words = docIDs_of_all_words + list(result_of_WordID[word].keys())
	
	rnd = dict(Counter(docIDs_of_all_words))
	
	sortedKeys = sorted(rnd, key=lambda key:rnd[key],reverse = True)
	rnd = {k:rnd[k] for k in sortedKeys}
	print("order of results")
	print(list(rnd.keys()))	