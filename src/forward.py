import json
import os
import string
from tqdm import tqdm
import collections
import numpy as np
from unidecode import unidecode
from nltk.stem.snowball import EnglishStemmer


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

def generateForwardIndex():

	with open('./dicts/lexicon.json', 'r', encoding="utf8") as lexfile:
		lexicon = json.load(lexfile)
	wordID = lexicon[list(lexicon.keys())[-1]] + 1		# get the last wordID in the lexicon,            															# add 1 to get wordID for next addition
	try:
		with open('forward.json', 'r', encoding="utf8") as docfile:
			docrepos = json.load(docfile)
	except FileNotFoundError:
		docrepos = dict()

	stemmer = EnglishStemmer()
	for file in tqdm(os.listdir(inDir)[:100]):		# run for 3 files to generate doc id with words and hits
		position = dict()
		docId = inDir[-3:] + file[-11:-5]			# unique docID for every blog

		with open(os.path.join(inDir,file),'r',encoding='utf8') as f:
			mydict = json.load(f)

		text = mydict['text']

		# remove punctuation from the text. Some hardcoding for Unicode characters
		punc = str.maketrans('', '', string.punctuation)
		dgts = str.maketrans('', '', string.digits)
		tokens = unidecode(text.lower()).replace('-', ' ').translate(punc).translate(dgts).split()
		tokens = [stemmer.stem(token) for token in tokens]
		
		for i in range(len(tokens)):
			tokens[i] = lexicon[tokens[i]]	          #convert words to their respective wordId

		for i in range(len(tokens)):	
			indexposition = getIndexPositions(tokens,tokens[i])		# get list with position of each element
			indexposition.insert(0,len(indexposition))				# insert hits of each word at the beginning
			position[tokens[i]] = indexposition						# storing list of hits and positions against wordID

		docrepos[docId] = position									# strong dictionary with wordID,hits and positing against docID

	with open("./dicts/forward.json",'w',encoding = "utf8") as docfile:     	# writing the dict into file
		json.dump(docrepos,docfile)