import json
import os
import string
from tqdm import tqdm

# path = 'D:/cs-250-semester-project/forward.json'

def generateInvertedIndex(dictDir):
	wordids = []
	inverted = dict()

	with open(os.path.join(dictDir, 'forward.json'), 'r', encoding="utf8") as findex:
		forward = json.load(findex)
	docids = list(forward.keys())		#get all docIds from forward index in a list

	with open(os.path.join(dictDir, "lexicon.json"), 'r', encoding="utf8") as lex:
		lexicon = json.load(lex)
	wordids = list(lexicon.values())
	wordids = list(map(str, wordids))

	for id in tqdm(wordids):
		indoc = dict()

		for doc in docids:

			if(forward[doc].get(id) == None):	#check if wordid exists in the subdictionary of docid
				continue						#go to next subdictionary if wordid is not present

			indoc[doc] = forward[doc][id]		# get hits and position from subdictionary and store it in new
												# dictionary with docid as key and hits and position as value
												
		inverted[id] = indoc					# store the subdictionary in another dictionary with wordid as key
	# print(inverted)
	with open(os.path.join(dictDir, "inverted.json"), 'w', encoding = "utf8") as docfile:     	#writing the dict into file
		json.dump(inverted, docfile, indent=2)