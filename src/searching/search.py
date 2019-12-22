import json
import os
import string
from config import *
from indexing.helper import *
from collections import Counter
from indexing.helper import *
import itertools
from datetime import datetime

def searchQuery(dictDir,query,lexicon):
	finalLongDocs = dict()
	finalShortDocs = dict()
	shortDocIDs = []
	longDocIDs = []
	finalResultList = []
	words = clean(query)
	#print (words)

	# finalLongDocs stores the sum of position decay for the word in all documents
	# longDocIDs stores the documents the word was found in

	for word in words:

		tempShortDocs , tempLongDocs = searchWord(dictDir,word,lexicon)
		
		# finalLongDocs = {key: finalLongDocs.get(key, 0) + tempLongDocs.get(key, 0)
		# 		for key in set(finalLongDocs) | set(tempLongDocs)}
		finalLongDocs = dict(Counter(finalLongDocs) + Counter(tempLongDocs))

		shortDocIDs = shortDocIDs + tempShortDocs

		longDocIDs = longDocIDs + list(tempLongDocs)


	# longResult counts the number of query words found in each document
	longResult = dict(Counter(longDocIDs))
	# shortResult counts the number of query words found in each document's author+title
	shortResult = dict(Counter(shortDocIDs))

	# sort shortResult by number of query words found in document. Remove
	# the documents that had fewer than len(words)-1 query words
	sortedKeys = sorted(shortResult, key=lambda key:shortResult[key],reverse = True)
	shortResult = {k:shortResult[k]*100000 for k in sortedKeys[:15] if shortResult[k] > len(words)-2}

	# sort longResult by number of query words found in document
	sortedKeys = sorted(longResult, key=lambda key:longResult[key],reverse = True)
	longResult = {k:longResult[k]*10000 + finalLongDocs[k] for k in sortedKeys[:15]}

	for key in set(shortResult).intersection(set(longResult)):
		longResult[key] += shortResult[key]

	# topShortResults = dict(itertools.islice(shortResult.items(), 15))
	# longResult = dict(itertools.islice(longResult.items(), 15))


	longResult = sorted(longResult, key=lambda key:longResult[key],reverse = True)
	# longResult = {k:longResult[k] for k in sortedKeys}	

	# print(topShortResults)
	print(longResult)

	# for shortDoc in list(topShortResults.keys()):
	# 	if topShortResults[shortDoc] == len(words):
	# 		finalResultList.append(shortDoc)
	# 	else:
	# 		break

	finalResultList = longResult # finalResultList + list(longResult.keys())
	
	print(datetime.now())
	print("order of results")

	if len(finalResultList) == 0:
		print("no result found")
	else:
		print(finalResultList)
		return finalResultList

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
