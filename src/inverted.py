import json
import os
import string
from tqdm import tqdm

# path = 'D:/cs-250-semester-project/forward.json'

def generateInvertedIndex(dictDir):
	"""
	parameters: dictDir - the path of the directory containing the
	dictionaries for the forward and the inverted index.

	This function will iterate through every wordID in the lexicon.
	For every wordID, it will subsequently iterate through every
	docID in the forward index, and will generate a dictionary
	containing the hits of that wordID in each document.
	
	This dictionary will then be added to the inverted index
	dictionary, which will be written to file.


	The inverted index is a dictionary of dictionaries of the form:
	{
		wordID : 
			{
				docID : [
					number of hits in this document,
					location of first hit,
					location of second hit,
					.
					.
					.
				],
				.
				.
				.
			},
		.
		.
		.
	}

	return: void
	"""
	wordIDs = []
	inverted = dict()

	with open(os.path.join(dictDir, 'forward.json'), 'r', encoding="utf8") as findex:
		forward = json.load(findex)
	docIDs = list(forward.keys())		# get all docIDs from forward index in a list

	with open(os.path.join(dictDir, "lexicon.json"), 'r', encoding="utf8") as lex:
		lexicon = json.load(lex)

	wordIDs = list(map(str, list(lexicon.values())))

	for wordID in tqdm(wordIDs):
		indoc = dict()

		for docID in docIDs:

			if(forward[docID].get(wordID) != None):	# do processing if wordID exists in the subdictionary of docID
			# get hits and position from subdictionary and store it in new dictionary with docID as key and hits and position as value								
				indoc[docID] = forward[docID][wordID]		

		inverted[wordID] = indoc					# store the subdictionary in another dictionary with wordID as key

	with open(os.path.join(dictDir, "inverted.json"), 'w', encoding = "utf8") as docfile:
		json.dump(inverted, docfile, indent=2)