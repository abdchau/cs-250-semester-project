import json
import os
import string
from config import *
from indexing.helper import *
from collections import Counter
from indexing.helper import *
import itertools
from datetime import datetime

def searchQuery(dictDir,query,lexicon,metadata):
	'''
		arguments:
			dictDir: path of dictionaries stores
			query: search query written in search bar
			lexicon: lexicon to be used to convert word into wordID
			metadata: for adding weighted shares. It is stored in 
			the form:
			the form:
			{
				docID : 
					{
						title
						author
						URL
						weightedShares
						file path
					},
				...
			}
		this function first gets all the docIDs from short
		barrels to check if query words are present in document's
		author or title and then gets gets all the documentIDs
		for each word, makes a dictionary with all documents
		against the number of words from query it is in and
		use this order along with weightedShares and 
		positionDecay of eachWord in each document
		to arrange document position in final result
		then select the top 15 results


	returns top 15 - 30 results
	'''
	# finalLongDocs stores the sum of position decay for the word in all documents
	# longDocIDs stores the documents the word was found in long barrels
	# shortDocIDs stores the documents the word was found in short barrels
	finalLongDocs = dict()
	shortDocIDs = []
	longDocIDs = []
	words = clean(query)

	if not words:
		return

	for word in words:

		tempShortDocs , tempLongDocs = searchWord(dictDir,word,lexicon)
		finalLongDocs = dict(Counter(finalLongDocs) + Counter(tempLongDocs))

		shortDocIDs = shortDocIDs + tempShortDocs
		longDocIDs = longDocIDs + list(tempLongDocs)


	# longResult holds document against number of query words found
	longResult = dict(Counter(longDocIDs))
	# shortResult holds document against number of query words found in author+title
	shortResult = dict(Counter(shortDocIDs))

	# limit is the factor by which we will remove documents results from shortResults
	if len(words) > 3:
		limit = len(words)-2*(len(words)//4)
	else:
		limit = len(words)-1

	# select top 15 results from shortResult and sort them by number of query words found in document.
	# Remove the documents that had fewer than limit query words
	sortedKeys = sorted(shortResult, key=lambda key:shortResult[key],reverse = True)
	shortResult = {k:shortResult[k]*15000 for k in sortedKeys[:15] if shortResult[k] > limit}

	# select top 15 results from longResult and sort them by number of query words found in document after adding 
	# weightages of shares and positionDecay from metaData
	sortedKeys = sorted(longResult, key=lambda key:longResult[key],reverse = True)
	longResult = {k:longResult[k]*10000 + finalLongDocs[k] + metadata[k][3] for k in sortedKeys[:15]}

	# insert the uncommon elements of shortResult into longResult 
	for key in shortResult:
		if longResult.get(key) is not None:
			longResult[key] += shortResult[key]
		else:
			longResult[key] = shortResult[key]

	# sort the longResult again to get final order of dsiplaying result
	sortedKeys = sorted(longResult, key=lambda key:longResult[key],reverse = True)
	longResult = {key:longResult[key] for key in sortedKeys}	
	
	if not longResult:
		return
	
	return longResult
		

def searchWord(dictDir,word,lexicon):

	'''
		arguments:
			-dictDir: path of directory containing inverted barrels
			-word: single word to search docIDs
			- lexicon: to convert word word into respective WordID
		
		this function generates list of documentIDs 
		from short barrels and dictionary of documentIDs 
		against its weightedShares from long barrels

	returns shortHitsDocs and longHitsIndex		
	'''
	shortHitsDocs = []
	longHitsIndex = dict()	

	# return empty list and empty dictionary if word is not found in lexicon
	try:
		wordID = lexicon[word]
	except KeyError:
		return shortHitsDocs,longHitsIndex
	
	# get barrel number from wordID for short barrels and get list of docIDs
	barrel = getBarrel(wordID)
	path = os.path.join(dictDir, 'short_inverted_barrels')
	shortHitsDocs = getAllDocs(path,barrel,wordID,short = True)

	# get dictionary of docIDs and positionDecay
	path = os.path.join(dictDir, 'inverted_barrels')
	longHitsIndex = getAllDocs(path,barrel,wordID,short = False)

	#return list and dictionary
	return shortHitsDocs,longHitsIndex

def getAllDocs(path,barrel,wordID,short = False):

	'''
		arguments:
			-path: path to open inverted barrels
			-barrel: barrel number where wordID is stored
			-wordID: wordID to retrive weightedShares
				from inverted barrels
			short: to indicate whether processing is for short 
				or long barrels


		this function returns list of documentIDs
		for short barrels or a dictoinary with
	 	documentIDs and their respective positionDecay			
	'''

	hitsIndex = dict()
	with open(os.path.join(path, f"inverted_{barrel}.json"), 'r', encoding = "utf8") as invBarrel:
		inverted = json.load(invBarrel)
		
	# return empty list or empty dictionary if word not found in iverted barrel	
	try:
		docIDs = list(inverted[str(wordID)].keys())
	except Exception as e:
		if short:
			emptyList = []
			return emptyList
		else:
			emptyDict = dict()
			return emptyDict	

	# return list of docIDs for short barrels
	if short:
		return docIDs

	# generate dictionary with docIDs and positionDecay and return for long barrel	
	for docID in docIDs:
		hitsIndex[docID] = inverted[str(wordID)][str(docID)]
	
	return hitsIndex
