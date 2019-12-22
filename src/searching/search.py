import json
import os
import string
from config import *
from indexing.helper import *
from collections import Counter
from indexing.helper import *
import itertools
from datetime import datetime

def searchquery(dictDir,query,lexicon):
	finalLongDocs = dict()
	finalShortDocs = dict()
	shortDocIDs = []
	longDocIDs = []
	finalResultList = []
	words = clean(query)
	#print (words)

	for word in words:

		tempShortDocs , tempLongDocs = searchWord(dictDir,word,lexicon)
		
		finalLongDocs = {key: finalLongDocs.get(key, 0) + tempLongDocs.get(key, 0)
				for key in set(finalLongDocs) | set(tempLongDocs)}

		shortDocIDs = shortDocIDs + tempShortDocs

		longDocIDs = longDocIDs + list(tempLongDocs.keys())


	
	longResult = dict(Counter(longDocIDs))
	shortResult = dict(Counter(shortDocIDs))

	sortedKeys = sorted(shortResult, key=lambda key:shortResult[key],reverse = True)
	shortResult = {k:shortResult[k] for k in sortedKeys}

	sortedKeys = sorted(longResult, key=lambda key:longResult[key],reverse = True)
	longResult = {k:longResult[k] for k in sortedKeys}

	topShortResults = dict(itertools.islice(shortResult.items(), 15))
	topLongResults = dict(itertools.islice(longResult.items(), 15))

	for doc in list(topLongResults.keys()):
		topLongResults[doc] = topLongResults[doc]*10000 + finalLongDocs[doc]

	sortedKeys = sorted(topLongResults, key=lambda key:topLongResults[key],reverse = True)
	topLongResults = {k:topLongResults[k] for k in sortedKeys}	

	print(topShortResults)
	print(topLongResults)

	for shortDoc in list(topShortResults.keys()):
		if topShortResults[shortDoc] == len(words):
			finalResultList.append(shortDoc)
		else:
			break

	finalResultList = finalResultList + list(topLongResults.keys())
	
	print(datetime.now())
	print("order of results")

	if len(finalResultList) == 0:
		print("no result found")
	else:
		print(finalResultList)

def searchWord(dictDir,word,lexicon):
	shortHitsDocs = []
	longHitsIndex = dict()	

	try:
		wordID = lexicon[word]
	except KeyError:
		return shortHitsDocs,longHitsIndex
	
	barrel = getBarrel(wordID)
	path = os.path.join(dictDir, 'short_inverted_barrels')

	shortHitsDocs = getAllDocs(path,barrel,wordID,short = True)

	path = os.path.join(dictDir, 'inverted_barrels')

	longHitsIndex = getAllDocs(path,barrel,wordID,short = False)

	return shortHitsDocs,longHitsIndex

def getAllDocs(path,barrel,wordID,short = False):

	hitsIndex = dict()
	with open(os.path.join(path, f"inverted_{barrel}.json"), 'r', encoding = "utf8") as invBarrel:
		inverted = json.load(invBarrel)
		
	try:
		docIDs = list(inverted[str(wordID)].keys())
	except Exception as e:
		if short:
			emptyList = []
			return emptyList
		else:
			emptyDict = dict()
			return emptyDict	
	
	if short:
		return docIDs

	for docID in docIDs:
		hitsIndex[docID] = inverted[str(wordID)][str(docID)]
	
	return hitsIndex
