import json
import os
import string
from tqdm import tqdm
import collections
import numpy as np
from unidecode import unidecode
from nltk.stem.snowball import EnglishStemmer
from multiprocessing import Process, Lock


def getIndexPositions(listOfElements, element):
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

def processFile(lexicon, forwardIndex, tokens, docID):
	"""
	parameters: lexicon - the lexicon to be used for indexing

	forwardIndex - the dictionary in which the forward index
	is to be stored

	file - the file whose forward index is to be generated

	lock - the multiprocessing lock. This must be acquired
	before adding data to the forwardIndex to maintain data
	integrity.

	returns: void

	This function expects to be called by multiple threads.
	"""

	position = dict()
	
	for i in range(len(tokens)):
		tokens[i] = lexicon[tokens[i]]	          #convert words to their respective wordId

	for i in range(len(tokens)):
		if tokens[i] is not None:										#  do processing if there is a word in list
			indexposition = getIndexPositions(tokens,tokens[i])		# get list with position of each element
			indexposition.insert(0,len(indexposition))				# insert hits of each word at the beginning
			position[tokens[i]] = indexposition						# storing list of hits and positions against wordID
			
			for index in indexposition:								# remove the repeated words in list
				tokens[index] = None
	

	forwardIndex[docID] = position				# storing dictionary with wordID, hits and locations against docID


def generateForwardIndex(cleanDir, dictDir):
	"""
	parameters: cleanDir - the path of the directory containing
	processed documents.

	dictDir - the path of the directory containing the dictionaries
	for the lexicon and the forward index.

	This function will iterate through every file in the given
	cleaned directory and using the lexicon, will generate
	the forward index. For each file, a dictionary will be
	generated and added to the forward index dictionary.

	The forward index is a dictionary of dictionaries of the form:
	{
		docID : 
			{
				wordID : [
					number of hits of this word,
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

	This function expects to be called by the main thread
	"""
	with open(os.path.join(dictDir, 'lexicon.json'), 'r', encoding="utf8") as lexfile:
		lexicon = json.load(lexfile)
	try:
		with open(os.path.join(dictDir, 'forward.json'), 'r', encoding="utf8") as docfile:
			forwardIndex = json.load(docfile)
	except FileNotFoundError:
		forwardIndex = dict()

	lock = Lock()
	processes = []
	for file in tqdm(os.listdir(cleanDir)):
		processes.append(Process(target=processFile, 
			args=(lexicon, forwardIndex, os.path.join(cleanDir, file))))
		processes[-1].start()
		
		# processFile(lexicon, forwardIndex, os.path.join(cleanDir, file))
		if len(processes) > 1:
			for p in processes:
				p.join()

	for p in processes:
		p.join()

	with open(os.path.join(dictDir, 'forward.json'), 'w', encoding = "utf8") as docfile:
		json.dump(forwardIndex,docfile, indent=2)

def dump(dictDir, forwardIndex):
	with open(os.path.join(dictDir, 'forward.json'), 'w', encoding = "utf8") as forwardFile:
		json.dump(forwardIndex, forwardFile, indent=2)
