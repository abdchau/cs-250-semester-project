import json
import os
from tqdm import tqdm
import collections


def getHits(listOfElements, element):
    ''' Returns the indexes of all occurrences of give element in
    the list- listOfElements '''
    indexPosList = []
    indexPos = 0
    while True:
        try:
            # Search for item in list from indexPos to the end of list
            indexPos = listOfElements.index(element, indexPos)
            # Add the index position in list
            indexPosList.append(indexPos)
            indexPos += 1
        except ValueError as e:
            break
 
    return indexPosList

def processFile(lexicon, forwardBarrels, barrelLength, tokens, docID):
	"""
	arguments:
		- lexicon: the lexicon to be used for indexing
		- forwardBarrels: the dictionary in which the forward 
		indices are to be stored. Each forward index is of 
		the form:
		{
			docID : 
				{
					wordID : [
						number of hits of this word,
						location of first hit,
						location of second hit,
						...
					],
					...
				},
			...
		}
		- barrelLength: the range of words in one barrel
		- tokens: the cleaned words in the file
		- docID: the unique ID assigned to the file

	This function will add hits for every word present in
	the file to the correct dictionary according to barrel
	number, docID and wordID

	returns: None
	"""
	for i in range(len(tokens)):

		if tokens[i] is not None:

			# choose barrel
			barrel = lexicon[tokens[i]]//barrelLength


			# prepare dictionary for hits insertion
			if forwardBarrels.get(barrel) is None:
				forwardBarrels[barrel] = dict()
			if forwardBarrels[barrel].get(docID) is None:
				forwardBarrels[barrel][docID] = dict()

			# insert the hits
			hits = getHits(tokens,tokens[i])
			forwardBarrels[barrel][docID][lexicon[tokens[i]]] = hits
			
			# remove the repeated words in list
			for index in hits:
				tokens[index] = None


def dump(dictDir, forwardBarrels):
	"""
	arguments:
		- dictDir: the path of the directory containing the
		dictionaries for the lexicon and the forward index.
		- forwardBarrels: the dictionary in which the forward
		indices are stored. The form is described above.

	This function will iterate through the forward barrels
	and will write each to file.

	return: None
	"""
	path = os.path.join(dictDir, 'forward_barrels')
	os.makedirs(path, exist_ok=True)
	
	for barrel, forwardIndex in enumerate(forwardBarrels.values()):
		with open(os.path.join(path, f'forward_{barrel}.json'), 'w', encoding = "utf8") as forwardFile:
			json.dump(forwardIndex, forwardFile, indent=2)